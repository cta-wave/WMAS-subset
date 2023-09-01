'''
Checking out sepcific snapshot of git repositry for each test group
and get the creation date of each tests in the group.
Save the creation date infomration for all tests to a json file.
'''
import requests
import git
import os
import shutil

from file_utility import read_json_file, write_json_to_file


def send_request(request_api):
    '''Send api request and return json report'''
    response = requests.get(request_api)
    if (response.status_code == 200):
        return response.json()
    else:
        print('Error in sending request:', request_api,
              ' response status:', response.status_code)


def get_all_tests(url: str):
    '''Get list of all tests from server'''
    test_list_url = url + 'api/tests'
    all_tests = send_request(test_list_url)

    # regroup the tests for css api
    css_tests = all_tests.pop('css')
    for css_test in css_tests:
        key = css_test.split('/')[1] + '/' + css_test.split('/')[2]
        if key not in all_tests.keys():
            all_tests[key] = []
        all_tests[key].append(css_test)
        
    return all_tests


def get_path_ready(version: str):
    '''get local path ready for the versions'''
    if os.path.isdir(version):
        shutil.rmtree(version)
        os.mkdir(version)
    else:
        os.mkdir(version)


def checkout_tests_from_repo(version: str, github_data: dict):
    '''clone and checkout tests from repo'''
    for key in github_data:
        repo = github_data[key]
        local_path = version + '/' + repo['local_path']
        git_path = repo['git_path']
        if os.path.isdir(version):
            print(f'Clone {key} git repositry: {git_path} to {local_path}')
            git_handler = git.Repo.clone_from(git_path, local_path)
        commit = repo['commit']
        if isinstance(commit, str):
            print('Checking out:', commit)
            git_handler.git.checkout(commit)


def get_test_creation_date(
    version: str, github_data: dict, url: str, out_put_file: str
):
    '''get creation date for slected version'''
    all_tests = get_all_tests(url)

    data = {}
    for api_name in all_tests.keys():
        print('Processing api', api_name, '...')

        if (
            api_name == 'webgl' or
            api_name == 'ecmascript' or
            api_name == 'wave-extra'
        ):
            g = git.Git(
                version + '/' + github_data[api_name]['local_path']
            )
        else:
            wpt_commit = github_data['wpt']['commit']
            wpt_local_path = version + '/' + github_data['wpt']['local_path']
            wpt_repo = git.Repo(wpt_local_path)
            # if more than one commit to checkout
            if isinstance(wpt_commit, dict):
                if api_name in wpt_commit.keys():
                    commit = wpt_commit[api_name]
                    print('Checking out for', api_name, commit, '...')
                    wpt_repo.git.checkout(commit)
            g = git.Git(wpt_local_path)

        for test in all_tests[api_name]:
            # remove '/' and the begining
            test_file_path = test[1:]
            # Discard anything after and include '?'
            test_file_path = test_file_path.split('?')[0]

            if api_name == 'webgl':
                test_file_path = test_file_path.replace('webgl/conformance-suite', 'conformance-suites/1.0.3')
            elif api_name == 'ecmascript':
                test_file_path = test_file_path.replace('ecmascript/tests', 'test')
            elif api_name == 'wave-extra':
                test_file_path = test_file_path.replace('wave-extra/', '')
            elif api_name == '2dcontext' and version != '2018':
                test_file_path = test_file_path.replace('2dcontext', 'html/canvas/element')

            # replace .html with relavent .js
            test_file_path = test_file_path.replace(".window.html", ".window.js")
            test_file_path = test_file_path.replace(".any.worker.html", ".any.js")
            test_file_path = test_file_path.replace(".any.serviceworker.html", ".any.js")
            test_file_path = test_file_path.replace(".any.sharedworker.html", ".any.js")
            test_file_path = test_file_path.replace(".worker.html", ".worker.js")
            test_file_path = test_file_path.replace(".any.html", ".any.js")

            try:
                creation_date = g.log('--follow', '--format=%aD', test_file_path).splitlines()[-1]
            except:
                try:
                    creation_date = g.log('--follow', '--format=%aD', test_file_path.replace('.html', '.js')).splitlines()[-1]
                except:
                    print('Unable to find creation date for', test)
                    creation_date = ''

            data[test] = creation_date
            write_json_to_file(out_put_file, data)


def process_wams_2018(github_data: dict):
    '''process wmas2018'''
    print('Getting test creation date for wmas2018 tests.')
    url = 'https://webapitests2018.ctawave.org/wave/'
    version = '2018'
    out_put_file = 'WMAS2018_test_creation_date.json'

    get_path_ready(version)
    checkout_tests_from_repo(version, github_data)
    get_test_creation_date(version, github_data, url, out_put_file)


def process_wams_2019(github_data: dict):
    '''process wmas2019'''
    print('Getting test creation date for wmas2019 tests.')
    url = 'https://webapitests2019.ctawave.org/wave/'
    version = '2019'
    out_put_file = 'WMAS2019_test_creation_date.json'

    get_path_ready(version)
    checkout_tests_from_repo(version, github_data)
    get_test_creation_date(version, github_data, url, out_put_file)


def process_wams_2021(github_data: dict):
    '''process wmas2021'''
    print('Getting test creation date for wmas2021 tests.')
    url = 'https://webapitests2021.ctawave.org/_wave/'
    version = '2021'
    out_put_file = 'WMAS2021_test_creation_date.json'

    get_path_ready(version)
    checkout_tests_from_repo(version, github_data)
    get_test_creation_date(version, github_data, url, out_put_file)


def main():
    '''Entry point.'''
    github_data = read_json_file('github_data.json')
    process_wams_2018(github_data['2018'])
    process_wams_2019(github_data['2019'])
    process_wams_2021(github_data['2021'])


if __name__ == '__main__':
    main()
 