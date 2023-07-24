'''
Output a list of selected subset of tests in a json file
'''
import hashlib
import requests
import os.path
from datetime import datetime

from file_utility import (
    read_json_file, write_json_to_file, write_report_to_file
)


def send_request(request_api):
    '''Send api request and return json report'''
    response = requests.get(request_api)
    if (response.status_code == 200):
        return response.json()
    else:
        print('Error in sending request:', request_api,
              ' response status:', response.status_code)

  
def read_results(url: str, token: str):
    '''Read result for given session token'''
    result_api_url = url + 'api/results/' + token
    
    results = send_request(result_api_url)

    return_results = {}

    for api in results:
        for result in results[api]:
            if api not in return_results:
                return_results[api] = []
            return_results[api].append(result)
    return return_results

        
def read_common_passed_tests(url: str, tokens: str):
    '''
    STEP 1: Start from the set of tests that pass on the reference browser versions 
    and existed at the appropriate cut-off date for the WMAS version to be tested
    STEP 2: Assume that set of tests that pass on the reference browser versions
    not include any manual test.
    '''
    session_results = []

    for token in tokens:
        session_result = read_results(url, token)
        session_results.append(session_result)

    passed_tests = []
    failed_tests = []

    for result in session_results:
        for api in result:
            for api_result in result[api]:
                passed = True
                for subtest in api_result['subtests']:
                    if subtest['status'] == 'PASS':
                        continue
                    passed = False
                    break

                test = api_result['test']

                if passed:
                    if test in failed_tests:
                        continue
                    if test in passed_tests:
                        continue
                    passed_tests.append(test)
                else:
                    if test in passed_tests:
                        passed_tests.remove(test)
                    if test in failed_tests:
                        continue
                    failed_tests.append(test)

    return passed_tests


def eliminate_block(tests, block_list):
    '''
    STEP 3: Eliminate any specific tests identified on a 
    manually curated ‘block’ list
    '''
    for test in block_list:
        if test in tests:
            tests.remove(test)
    
    return tests


def select_test_by_random_hashing(test_names,
                                  cut_off_age,
                                  percentage_of_recent,
                                  percentage_of_established,
                                  creation_date_data,
                                  published_date):
    '''
    STEP 4: Select tests by random (but repeatable) hashing and 
    whether tests can be classified as "established" or "recent"
    '''
    selected_tests = []
    count = 0
    for test_path in test_names:
        test_name = test_path[test_path.rfind('/')+1: test_path.rfind('.html')]
        my_hash = int.from_bytes(hashlib.sha256(test_name.encode('utf-8')).digest(), 'big')
        test_code = my_hash % 1000

        try:
            creation_date_str = creation_date_data[test_path]
            creation_date = datetime.strptime(creation_date_str, '%a, %d %b %Y %H:%M:%S %z')
            test_age = (published_date - creation_date).days
        except:
            test_age = 0
        
        # exclude tests created after the published
        if test_age > 0:
            if test_age <= cut_off_age:
                if test_code < 10 * percentage_of_recent:
                    selected_tests.append(test_path)
                    count += 1
            else:
                if test_code < 10 * percentage_of_established:
                    selected_tests.append(test_path)
                    count += 1

    return selected_tests


def add_back_must_include(selected_tests, must_include_list):
    '''
    STEP 5: manually curated ‘must include’ list
    '''
    for test in must_include_list:
        if test not in selected_tests:
            selected_tests.append(test)
    
    return selected_tests


def get_common_passed_test(reference_results: list, api_name: str) -> list:
    '''Return common passed test for seleceted api name'''
    common_passed_test = []
    api_path = "/" + api_name
    for result in reference_results:
        if result.startswith(api_path):
            common_passed_test.append(result)
    return common_passed_test


def process_subsetting(
         version: str, published_date: str, server_url: str
    ):
    '''Process Subsetting'''
    test_creation_date_file = 'WMAS' + version + '_test_creation_date.json'
    input_file = 'WMAS' + version + '_input.json'
    report_file = 'WMAS' + version + '_subset_report.csv'
    output_file = 'WMAS' + version + '_subset_of_tests.json'

    # get test age from 'test_creation_date.json'
    if os.path.exists(test_creation_date_file):
        creation_date_data = read_json_file(test_creation_date_file)
    else:
        print('Error:', test_creation_date_file, 'does not present. ')
        print('Please run "get_test_creation_date.py" first to get test age for all tests.')
        return
    
    input_data = read_json_file(input_file)

    session_api_url = server_url + 'api/sessions/public'
    reference_tokens = send_request(session_api_url)
    
    print('Getting common passed tests for reference browsers: ', reference_tokens)
    reference_results = read_common_passed_tests(server_url, reference_tokens)

    data = {}
    report = []
    for api_name in input_data:
        print('Processing ', api_name, '...')

        api_input_data = input_data[api_name]
        cut_off_age = api_input_data['cut_off_age']
        percentage_of_recent = api_input_data['percentage_of_recent']
        percentage_of_established = api_input_data['percentage_of_established']
        block_list = api_input_data['block_list']
        must_include_list = api_input_data['must_include_list']

        # start from common passed tests for reference browsers
        api_tests = get_common_passed_test(reference_results, api_name)
        # eliminate tests in block list
        api_tests_after_eliminate_block = eliminate_block(api_tests, block_list)
        # select random test by weight
        selected_tests_by_random_hashing = select_test_by_random_hashing(api_tests_after_eliminate_block,
                                                       cut_off_age*365,
                                                       percentage_of_recent,
                                                       percentage_of_established,
                                                       creation_date_data,
                                                       published_date)
        # add back must include tests
        selected_tests = add_back_must_include(selected_tests_by_random_hashing, must_include_list)
        selected_tests.sort()
        data[api_name] = selected_tests

        report.append([api_name,cut_off_age, percentage_of_recent, 
                      percentage_of_established, block_list, must_include_list,
                      len(api_tests), len(selected_tests)])

    header = ['API Name', 'Cut Off Age(year)',
              'Percentage Of Recent', 'Percentage Of Established',
              'Block List', 'Must Include List',
              'Number of Common Passed Tests', 'Selected Test Count']
    write_report_to_file(report_file, header, report)
    write_json_to_file(output_file, data)


def wmas2018_subsetting():
    '''subsetting for wmas2018'''
    version = '2018'
    published_date = datetime.strptime('2018/12/13 00:00:00 +0000', '%Y/%m/%d %H:%M:%S %z')
    server_url = 'https://webapitests' + version +'.ctawave.org/wave/'
    process_subsetting(version, published_date, server_url)


def wmas2019_subsetting():
    '''subsetting for wmas2019'''
    version = '2019'
    published_date = datetime.strptime('2019/12/04 00:00:00 +0000', '%Y/%m/%d %H:%M:%S %z')
    server_url = 'https://webapitests' + version +'.ctawave.org/wave/'
    process_subsetting(version, published_date, server_url)


def wmas2021_subsetting():
    '''subsetting for wmas2021'''
    version = '2021'
    published_date = datetime.strptime('2021/12/14 00:00:00 +0000', '%Y/%m/%d %H:%M:%S %z')
    server_url = 'https://webapitests' + version +'.ctawave.org/_wave/'
    process_subsetting(version, published_date, server_url)


def main():
    '''Entry point.'''
    wmas2018_subsetting()
    wmas2019_subsetting()
    wmas2021_subsetting()


if __name__ == '__main__':
    main()
 