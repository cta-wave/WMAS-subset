'''
Output a list of excluded tests in a json file
'''
import json
import requests


def send_request(request_api) -> None:
    '''Send api request and return json report'''
    response = requests.get(request_api)
    if (response.status_code == 200):
        return response.json()
    else:
        print('Error in sending request:', request_api,
              ' response status:', response.status_code)


def get_all_tests(server_url: str) -> None:
    '''Get list of all tests from WMAS server'''
    test_list_url = server_url + 'api/tests'
    all_tests = send_request(test_list_url)

    # regroup the tests for css api
    css_tests = all_tests.pop('css')
    for css_test in css_tests:
        key = css_test.split('/')[1] + '/' + css_test.split('/')[2]
        if key not in all_tests.keys():
            all_tests[key] = []
        all_tests[key].append(css_test)
        
    return all_tests


def write_json_to_file(file_name: str, data: dict) -> None:
    '''Write JSON date to a file'''
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile, indent=4, separators=(',', ': '), default=str)


def read_json_file(file_name: str) -> dict:
    '''Read date from a json file'''
    with open(file_name, 'rt') as file:
        data = json.load(file)
    return data


def get_excluded_tests(version: str, server_url: str):
    '''get excluded tests'''
    subset_file = 'WMAS' + version + '_subset_of_tests.json'
    excluded_tests_file = 'WMAS' + version + '_excluded_tests.json'

    excluded_tests = []
    #Get list of all tests from WMAS server'''
    all_tests = get_all_tests(server_url)
    for api in all_tests:
        excluded_tests.extend(all_tests[api])

    # read subset json file
    subset_data = read_json_file(subset_file)

    for api_name in subset_data:
        print('Processing ', api_name, '...')
        api_subset_data = subset_data[api_name]
        for selected_test in api_subset_data:
            for test_path in excluded_tests:
                if selected_test == test_path:
                    excluded_tests.remove(test_path)
                    break

    write_json_to_file(excluded_tests_file, excluded_tests)


def wmas2018_get_excluded_tests():
    version = "2018"
    server_url = 'https://webapitests2018.ctawave.org/wave/'
    get_excluded_tests(version, server_url)


def wmas2019_get_excluded_tests():
    version = "2019"
    server_url = 'https://webapitests2019.ctawave.org/wave/'
    get_excluded_tests(version, server_url)


def wmas2021_get_excluded_tests():
    version = "2021"
    server_url = 'https://webapitests2021.ctawave.org/_wave/'
    get_excluded_tests(version, server_url)


def main():
    '''Entry point.'''
    wmas2018_get_excluded_tests()
    wmas2019_get_excluded_tests()
    wmas2021_get_excluded_tests()

if __name__ == '__main__':
    main()