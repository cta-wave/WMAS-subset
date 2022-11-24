'''
Output a list of selected subset of tests in a json file
'''
import hashlib
import requests
import json
import csv
import os.path
from datetime import datetime

# -------------------Manaul input parameters----------------------------

WMAS2019_SERVER_URL = 'https://webapitests2019.ctawave.org/wave/'
WMAS2019_published_date = '2019/12/04 00:00:00 +0000'

# further input parameters are defined in the following json file
INPUT_FILE = 'WMAS2019_input.json'

# -------------------End of manaul input parameters---------------------

def send_request(request_api):
    '''Send api request and return json report'''
    response = requests.get(request_api)
    if (response.status_code == 200):
        return response.json()
    else:
        print('Error in sending request:', request_api,
              ' response status:', response.status_code)

  
def read_results(token):
    '''Read result for given session token'''
    result_api_url = WMAS2019_SERVER_URL + 'api/results/' + token
    
    results = send_request(result_api_url)

    return_results = {}

    for api in results:
        for result in results[api]:
            if api not in return_results:
                return_results[api] = []
            return_results[api].append(result)
    return return_results

        
def read_common_passed_tests(tokens):
    '''
    STEP 1: Start from the set of tests that pass on the reference browser versions 
    and existed at the appropriate cut-off date for the WMAS version to be tested
    STEP 2: Assume that set of tests that pass on the reference browser versions
    not include any manual test.
    '''
    session_results = []

    for token in tokens:
        session_result = read_results(token)
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


def write_report_to_file(file_name: str, data: dict):
    '''Write subsetting report to a csv file'''
    header = ['API Name', 'Cut Off Age(year)',
              'Percentage Of Recent', 'Percentage Of Established',
              'Block List', 'Must Include List',
              'Number of Common Passed Tests', 'Selected Test Count']

    with open(file_name, 'w', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


def write_json_to_file(file_name: str, data: dict):
    '''Write JSON date to a file'''
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile, indent=4, separators=(',', ': '), default=str)


def read_json_file(file_name: str) -> dict:
    '''Read date from a json file'''
    with open(file_name, 'rt') as file:
        data = json.load(file)
    return data


def get_common_passed_test(reference_results: list, api_name: str) -> list:
    '''Return common passed test for seleceted api name'''
    common_passed_test = []
    api_path = "/" + api_name
    for result in reference_results:
        if result.startswith(api_path):
            common_passed_test.append(result)
    return common_passed_test


def main():
    '''Entry point.'''
    # get published date
    published_date = datetime.strptime(WMAS2019_published_date, '%Y/%m/%d %H:%M:%S %z')

    # get test age from 'test_creation_date.json'
    test_creation_date_file = 'test_creation_date.json'
    if os.path.exists(test_creation_date_file):
        creation_date_data = read_json_file(test_creation_date_file)
    else:
        print('Error:', test_creation_date_file, 'does not present. ')
        print('Please run "get_test_creation_date.py" first to get test age for all tests.')
        return
    
    input_data = read_json_file(INPUT_FILE)

    session_api_url = WMAS2019_SERVER_URL + 'api/sessions/public'
    reference_tokens = send_request(session_api_url)
    
    print('Getting common passed tests for reference browsers: ', reference_tokens)
    reference_results = read_common_passed_tests(reference_tokens)

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
        data[api_name] = selected_tests

        report.append([api_name,cut_off_age, percentage_of_recent, 
                      percentage_of_established, block_list, must_include_list,
                      len(api_tests), len(selected_tests)])

    write_report_to_file('subset_report.csv', report)
    write_json_to_file('subset_of_tests.json', data)


if __name__ == '__main__':
    main()
 