'''
Checking out sepcific snapshot of git repositry for each test group
and get the creation date of each tests in the group.
Save the creation date infomration for all tests to a json file.
'''
import requests
import json
import git

OUTPUT_JSON = 'test_creation_date.json'
WPT_LOCAL_CHECKOUT_PATH = 'wpt'

# -------------------Manaul input parameters----------------------------
WMAS2019_SERVER_URL = 'https://webapitests2019.ctawave.org/wave/'

WPT_GIT = 'https://github.com/web-platform-tests/wpt.git'
WPT_COMMITS = {
    'dom': 'cffa949fc9e0fcda9039f3275470ef7a663a7d6c',
    'websockets': 'b83ec322c2c9dbeba625d94351a69136f8584629',
    'webmessaging': '7287608f90f6b9530635d10086fd2ab386faab38',
    'webstorage': 'a5f707c18b3d893a6e332994064911c2f11e800d',
    'workers': '66e29f00f5ac4b42175342c15927b9efaf4dc19f',
    'encrypted-media': '5845bba1671bad710561b6b6e5825989878bb44c',
    'media-source': 'e0dc0f1a554ed116efa992a7095def76c58e13ee',
    'webaudio': '67152fdecd6e7955f934a4aec9a15407cbcfa3ac',
    'fullscreen': '7287608f90f6b9530635d10086fd2ab386faab38',
    'fetch': 'd3a7b003821596386fb708fe18decf696c563277',
    'xhr': '30cb639eaaa1c3bbd4eabee9c50685dc98cad2af',
    'content-security-policy': '94d018bb5d7c0d46df7ba1ac1efdbaa88bc159dc',
    'subresource-integrity': '8fefedccb9ae49bddd9c84d22b21177f156a561e',
    'upgrade-insecure-requests': 'b4b88e7de8f61c8c8fe1ac615fd883b3a042709f',
    'WebCryptoAPI': '14236258ece08c439179427a25f0a2102f5664df',
    'page-visibility': 'df24fb604e2d40528ac1d1b5dd970e32fc5c2978',
    'IndexedDB': 'b57479444fa21e2854dfb876f36f14f437ef7e35',
    'FileAPI': '648205dcf15d75c37b7abe7a0c1a2a7128baea36',
    'notifications': 'a5f707c18b3d893a6e332994064911c2f11e800d',
    'service-workers': 'b26c9dcf86ba2f91e2ea20ad72d67c0ce51b5b5d',
    'uievents': '66ec292ee48a9a2bbfa2f556e614926cd07211aa',
    'css/CSS2': '35979641de0b29313f7f28ab352d380186754ecd',
    'css/compositing': '5d0dcf0142d07916584db9c76c2fdec02833e959',
    'css/css-animations': 'f6acb6c0316cabf895c8c47dc654e77ef4b2a287',
    'css/css-backgrounds': '398cdfa444185dda88ca6e87fb12096bc8a82199',
    'css/css-ui': '545c96ead1616661ce2e97b66450efcf1b032851',
    'css/css-cascade': '84ec2ed74115b1c2ca72765b458f3a5d4da792dc',
    'css/css-color': 'b6e84edf4a398cc48f4983cbd8398858816996ae',
    'css/css-conditional': '01bda5c03bf8ae4ee00251b8969adf1ef69f443d',
    'css/css-variables': 'b1f24df9a2e449e0545bf6d74b62c0a40c543fde',
    'css/css-flexbox': '9d6f1c1aa7e1daa62c350b3fec18d594792f408a',
    'css/css-fonts': '3d83b8688bbd6d9e2a7fc31021bc214cbf0ebcb7',
    'css/css-grid': '94c4df86480774d00dbc9451eb4ffd9c4f3e233f',
    'css/css-images': '0624a18c9ebc3cc710d1e54dfd5adb5a0a829c42',
    'css/css-multicol': 'c0b406d151940c4253d59c041d895e763c27e754',
    'css/css-namespaces': '29f50c937e8be8ccf73dbb8b8e74f0668a1cd426',
    'css/css-style-attr': 'a5f707c18b3d893a6e332994064911c2f11e800d',
    'css/css-syntax': '3696f2233a37437896505b7187968aa605be9255',
    'css/css-transforms': '5f0da8e0ee156d0561ebcb9c9304dedd06119bd8',
    'css/css-transitions': '2ed850a370f099478001a7ae6bb765d38dab8057',
    'css/css-values': '861e227caba7dc9341dd833518f0d01b1e02d0a4',
    'css/css-writing-modes': '1799625e205a4457d879b6b9a3f74365f3b9cfd3',
    'css/cssom-view': '3806bf2419e25bd57e70b42103478fd3c12a143b',
    'css/filter-effects': '98ed5928328dd2121d13752ec7c84e1e29c39f4b',
    'css/mediaqueries': 'b09e7e2e78695b5e2052bfadd941de602f1e16fb',
    'css/selectors': 'eff766e5c8c39be7b9bff064bce3a18eb2953ac5',
    'html': 'db2276bb4b19da6818db5301b49dcbbc3f4c136e',
    'html/canvas/element': '178b6bcde9cbb1d8e04076fe59c86ea94f122964',
}

# -------------------End of manaul input parameters---------------------
def send_request(request_api):
    '''Send api request and return json report'''
    response = requests.get(request_api)
    if (response.status_code == 200):
        return response.json()
    else:
        print('Error in sending request:', request_api,
              ' response status:', response.status_code)


def write_json_to_file(file_name: str, data: dict):
    '''Write JSON date to a file'''
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile, indent=4, separators=(',', ': '), default=str)


def get_all_tests():
    '''Get list of all tests for WMAS2019 server'''
    test_list_url = WMAS2019_SERVER_URL + 'api/tests'
    all_tests = send_request(test_list_url)

    # regroup the tests for css api
    css_tests = all_tests.pop('css')
    for css_test in css_tests:
        key = css_test.split('/')[1] + '/' + css_test.split('/')[2]
        if key not in all_tests.keys():
            all_tests[key] = []
        all_tests[key].append(css_test)
        
    return all_tests


def main():
    '''Entry point.'''
    # clone wpt git repositry
    print('Clone wpt git repositry:', WPT_GIT, 'to', WPT_LOCAL_CHECKOUT_PATH)
    wpt_repo = git.Repo.clone_from(WPT_GIT, WPT_LOCAL_CHECKOUT_PATH)
    wpt_repo = git.Repo(WPT_LOCAL_CHECKOUT_PATH)

    all_tests = get_all_tests()

    data = {}
    for api_name in all_tests.keys():
        print('Processing', api_name, '...')

        if api_name == '2dcontext':
            commit = WPT_COMMITS['html/canvas/element']
        elif api_name in WPT_COMMITS.keys():
            commit = WPT_COMMITS[api_name]
        
        print('Checking out', commit, '...')
        wpt_repo.git.checkout(commit)
        g = git.Git(WPT_LOCAL_CHECKOUT_PATH)

        for test in all_tests[api_name]:
            if api_name == '2dcontext':
                test_file_path = test.replace('/2dcontext', 'html/canvas/element')
            else:
                test_file_path = test[1:]

            try:
                creation_date = g.log('--format=%aD', test_file_path).splitlines()[-1]
            except:
                creation_date = ''

            data[test] = creation_date
            write_json_to_file(OUTPUT_JSON, data)


if __name__ == '__main__':
    main()
 