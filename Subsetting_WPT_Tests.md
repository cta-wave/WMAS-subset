# Subsetting WPT Tests
WPT subsetting is aim to confirm that a sufficiently recent browser has been integrated, verify that the browser has been properly integrated and be able to run the required tests within a manageable test run time. Number or proportion of tests needed depends on the web standard being tested. Subsets need to be reproducible.

## Approach
The subsetting script takes following steps:
1. Start from the set of tests that pass on each of the reference browser versions and existed at the appropriate cut-off date for the WMAS version to be tested
2. Eliminate all manual tests (option to add back a small number of high priority tests at step 5 if this is considered essential)
3. Eliminate any specific tests identified on a manually curated ‘block’ list (e.g. tests that can’t be run on, or are not relevant to media consumption devices)
4. For each web standard being tested, select a pre-determined proportion of ‘established’ tests and a pre-determined proportion of ‘recent’ tests, appropriate to that web standard
5. Add any specific tests identified on a manually curated ‘must include’ list (e.g. tests for high priority APIs or APIs with known integration problems)

## Subsetting Algorithm
* Manually choose a threshold age at cut-off, AT, for a test to be considered “recent” or “established”
* For each WPT test grouping g, manually choose a percentage of “recent” tests to include, PR[g], and a percentage of “established” tests to include, PE[g]
* For each test t in grouping g that remains a candidate (see slide 5):
    * Calculate a SHA-256 hash, H[t] of its unique test name and derive H’[t] = H[t] mod 1000
    * Calculate the test’s age at the cut-off date, A[t]
    * If A[t] ≤ AT then include the test if H’[t] < 10 PR[g] else include the test if H’[t] < 10 PE[g]
* Using a hash of the test name gives consistent test selections if tests are added or removed from the upstream WPT and if AT, PR[g], PE[g] are changed

## Manual Input Required for Subsetting
Subsetting is done for WMAS2018, WMAS2019 and WMAS2021.

Following manual input required for subsetting and which is defined per WMAS version.
* Published date: Publication or snapshot date for WAMS specification
* Cut Off Age: Time period to consider for identifying “recent” tests
* Recent Percentage and Established Percentage: Subset percentage for each test group
* Block List and Must Include List: Specific tests (if any) to include on ‘block’ and ‘must include’ lists

### WMAS2018
Published date: 2018/12/13

| Test Group | Cut Off Age(year) | Recent Percentage |  Established Percentage | Block List | Must Include List | #Common Passed Tests | #Tests Selected |
| ---------- | ----------------- | ----------------- | ----------------------- | ---------- | ----------------- | -------------------- | --------------- |
| IndexedDB | 2 | 80 | 80 | [] | [] | 209 | 170 |
| WebCryptoAPI | 2 | 85 | 90 | [] | [] | 1 | 1 |
| webaudio | 2 | 15 | 35 | [] | [] | 86 | 14 |
| encrypted-media | 2 | 80 | 90 | [] | [] | 0 | 0 |
| websockets | 2 | 35 | 35 | [] | [] | 59 | 23 |
| fullscreen | 2 | 80 | 80 | [] | [] | 0 | 0 |
| xhr | 2 | 35 | 65 | [] | [] | 186 | 50 |
| webgl | 2 | 0 | 25 | [] | [] | 643 | 161 |
| html | 2 | 0 | 20 | [] | [] | 864 | 113 |
| webmessaging | 2 | 35 | 35 | [] | [] | 85 | 37 |
| service-workers | 2 | 100 | 100 | [] | [] | 75 | 75 |
| webstorage | 2 | 35 | 55 | [] | [] | 18 | 11 |
| css/compositing | 2 | 50 | 55 | [] | [] | 0 | 0 |
| css/css-animations | 2 | 50 | 55 | [] | [] | 0 | 0 |
| css/css-backgrounds | 2 | 50 | 55 | [] | [] | 5 | 2 |
| css/css-cascade | 2 | 50 | 55 | [] | [] | 0 | 0 |
| css/css-color | 2 | 50 | 55 | [] | [] | 0 | 0 |
| css/css-conditional | 2 | 50 | 55 | [] | [] | 0 | 0 |
| css/css-flexbox | 2 | 50 | 55 | [] | [] | 79 | 26 |
| css/css-fonts | 2 | 50 | 55 | [] | [] | 2 | 2 |
| css/css-images | 2 | 50 | 55 | [] | [] | 0 | 0 |
| css/css-multicol | 2 | 50 | 55 | [] | [] | 2 | 1 |
| css/css-syntax | 2 | 50 | 55 | [] | [] | 12 | 7 |
| css/css-transforms | 2 | 50 | 55 | [] | [] | 8 | 4 |
| css/css-transitions | 2 | 50 | 55 | [] | [] | 6 | 4 |
| css/css-ui | 2 | 50 | 55 | [] | [] | 1 | 0 |
| css/css-values | 2 | 50 | 55 | [] | [] | 1 | 0 |
| css/css-writing-modes | 2 | 50 | 55 | [] | [] | 0 | 0 |
| css/CSS2 | 2 | 50 | 55 | [] | [] | 14 | 8 |
| css/cssom-view | 2 | 50 | 55 | [] | [] | 24 | 14 |
| css/mediaqueries | 2 | 50 | 55 | [] | [] | 0 | 0 |
| css/selectors | 2 | 50 | 55 | [] | [] | 49 | 26 |
| page-visibility | 2 | 100 | 100 | [] | [] | 3 | 3 |
| 2dcontext | 2 | 5 | 10 | [] | [] | 633 | 71 |
| uievents | 2 | 100 | 100 | [] | [] | 6 | 6 |
| media-source | 2 | 90 | 95 | [] | [] | 2 | 2 |
| notifications | 2 | 100 | 100 | [] | [] | 1 | 1 |
| wave_extra | 2 | 50 | 50 | [] | [] | 0 | 0 |
| content-security-policy | 2 | 20 | 25 | [] | [] | 124 | 21 |
| dom | 2 | 35 | 35 | [] | [] | 194 | 68 |
| fetch | 2 | 35 | 35 | [] | [] | 59 | 25 |
| FileAPI | 2 | 100 | 100 | [] | [] | 8 | 8 |
| ecmascript | 2 | 35 | 35 | [] | [] | 13350 | 4600 |
| workers | 2 | 35 | 35 | [] | [] | 105 | 39 |


### WMAS2019
Published date: 2019/12/04
| Test Group | Cut Off Age(year) | Recent Percentage |  Established Percentage | Block List | Must Include List | #Common Passed Tests | #Tests Selected |
| ---------- | ----------------- | ----------------- | ----------------------- | ---------- | ----------------- | -------------------- | --------------- |
| 2dcontext | 2 | 100 | 100 | [] | [] | 723 | 0 |
| FileAPI | 2 | 100 | 100 | [] | [] | 23 | 4 |
| IndexedDB | 2 | 80 | 80 | [] | [] | 9 | 8 |
| WebCryptoAPI | 2 | 85 | 90 | [] | [] | 10 | 2 |
| content-security-policy | 2 | 20 | 25 | [] | [] | 160 | 28 |
| css/compositing | 2 | 50 | 55 | [] | [] | 11 | 6 |
| css/css-animations | 2 | 50 | 55 | [] | [] | 34 | 15 |
| css/css-backgrounds | 2 | 50 | 55 | [] | [] | 111 | 55 |
| css/css-cascade | 2 | 50 | 55 | [] | [] | 2 | 1 |
| css/css-color | 2 | 50 | 55 | [] | [] | 16 | 7 |
| css/css-conditional | 2 | 50 | 55 | [] | [] | 1 | 1 |
| css/css-flexbox | 2 | 50 | 55 | [] | [] | 171 | 39 |
| css/css-fonts | 2 | 50 | 55 | [] | [] | 72 | 39 |
| css/css-grid | 2 | 50 | 55 | [] | [] | 44 | 27 |
| css/css-images | 2 | 50 | 55 | [] | [] | 17 | 10 |
| css/css-multicol | 2 | 50 | 55 | [] | [] | 40 | 10 |
| css/css-namespaces | 2 | 50 | 55 | [] | [] | 0 | 0 |
| css/css-style-attr | 2 | 50 | 55 | [] | [] | 0 | 0 |
| css/css-syntax | 2 | 50 | 55 | [] | [] | 26 | 12 |
| css/css-transforms | 2 | 50 | 55 | [] | [] | 56 | 25 |
| css/css-transitions | 2 | 50 | 55 | [] | [] | 44 | 16 |
| css/css-ui | 2 | 50 | 55 | [] | [] | 54 | 26 |
| css/css-values | 2 | 50 | 55 | [] | [] | 44 | 17 |
| css/css-variables | 2 | 50 | 55 | [] | [] | 24 | 8 |
| css/css-writing-modes | 2 | 50 | 55 | [] | [] | 17 | 8 |
| css/CSS2 | 2 | 50 | 55 | [] | [] | 37 | 14 |
| css/cssom-view | 2 | 50 | 55 | [] | [] | 68 | 34 |
| css/filter-effects | 2 | 50 | 55 | [] | [] | 24 | 11 |
| css/mediaqueries | 2 | 50 | 55 | [] | [] | 1 | 0 |
| css/selectors | 2 | 50 | 55 | [] | [] | 96 | 28 |
| dom | 2 | 35 | 35 | [] | [] | 159 | 56 |
| ecmascript | 2 | 35 | 35 | [] | [] | 20367 | 7153 |
| encrypted-media | 2 | 80 | 90 | [] | [] | 11 | 10 |
| fetch | 2 | 35 | 35 | [] | [] | 52 | 21 |
| fullscreen | 2 | 80 | 80 | [] | [] | 0 | 0 |
| html | 2 | 0 | 20 | [] | [] | 1024 | 168 |
| manifest | 2 | 80 | 80 | [] | [] | 0 | 0 |
| media-source | 2 | 90 | 95 | [] | [] | 9 | 7 |
| notifications | 2 | 100 | 100 | [] | [] | 1 | 1 |
| page-visibility | 2 | 100 | 100 | [] | [] | 3 | 3 |
| service-workers | 2 | 100 | 100 | [] | [] | 5 | 4 |
| subresource-integrity | 2 | 100 | 100 | [] | [] | 1 | 1 |
| uievents | 2 | 100 | 100 | [] | [] | 5 | 5 |
| upgrade-insecure-requests | 2 | 55 | 55 | [] | [] | 55 | 0 |
| webaudio | 2 | 15 | 35 | [] | [] | 154 | 23 |
| webgl | 2 | 0 | 25 | [] | [] | 649 | 162 |
| webmessaging | 2 | 35 | 35 | [] | [] | 48 | 24 |
| websockets | 2 | 35 | 35 | [] | [] | 73 | 29 |
| webstorage | 2 | 35 | 55 | [] | [] | 26 | 13 |
| workers | 2 | 35 | 35 | [] | [] | 65 | 22 |
| xhr | 2 | 35 | 65 | [] | [] | 24 | 11 |


### WMAS2021
Published date: 2021/12/14
| Test Group | Cut Off Age(year) | Recent Percentage |  Established Percentage | Block List | Must Include List | #Common Passed Tests | #Tests Selected |
| ---------- | ----------------- | ----------------- | ----------------------- | ---------- | ----------------- | -------------------- | --------------- |
| 2dcontext | 2 | 5 | 10 | [] | [] | 733 | 37 |
| FileAPI | 2 | 100 | 100 | [] | [] | 60 | 40 |
| IndexedDB | 2 | 80 | 80 | [] | [] | 9 | 8 |
| WebCryptoAPI | 2 | 85 | 90 | [] | [] | 36 | 18 |
| beacon | 2 | 50 | 50 | [] | [] | 7 | 2 |
| content-security-policy | 2 | 20 | 25 | [] | [] | 291 | 74 |
| css/CSS2 | 2 | 50 | 55 | [] | [] | 38 | 23 |
| css/compositing | 2 | 50 | 55 | [] | [] | 11 | 6 |
| css/css-animations | 2 | 50 | 55 | [] | [] | 53 | 28 |
| css/css-backgrounds | 2 | 50 | 55 | [] | [] | 111 | 64 |
| css/css-cascade | 2 | 50 | 55 | [] | [] | 7 | 3 |
| css/css-color | 2 | 50 | 55 | [] | [] | 16 | 8 |
| css/css-conditional | 2 | 50 | 55 | [] | [] | 1 | 1 |
| css/css-easing | 2 | 50 | 50 | [] | [] | 2 | 0 |
| css/css-flexbox | 2 | 50 | 55 | [] | [] | 221 | 93 |
| css/css-font-loading | 2 | 50 | 50 | [] | [] | 6 | 2 |
| css/css-fonts | 2 | 50 | 55 | [] | [] | 75 | 46 |
| css/css-grid | 2 | 50 | 55 | [] | [] | 272 | 152 |
| css/css-images | 2 | 50 | 55 | [] | [] | 20 | 11 |
| css/css-multicol | 2 | 50 | 55 | [] | [] | 38 | 11 |
| css/css-scroll-snap | 2 | 50 | 50 | [] | [] | 41 | 22 |
| css/css-shapes | 2 | 50 | 50 | [] | [] | 78 | 41 |
| css/css-syntax | 2 | 50 | 55 | [] | [] | 27 | 12 |
| css/css-text-decor | 2 | 50 | 50 | [] | [] | 32 | 15 |
| css/css-transforms | 2 | 50 | 55 | [] | [] | 60 | 32 |
| css/css-transitions | 2 | 50 | 55 | [] | [] | 54 | 28 |
| css/css-ui | 2 | 50 | 55 | [] | [] | 66 | 39 |
| css/css-values | 2 | 50 | 55 | [] | [] | 47 | 27 |
| css/css-variables | 2 | 50 | 55 | [] | [] | 27 | 9 |
| css/css-will-change | 2 | 50 | 50 | [] | [] | 5 | 2 |
| css/css-writing-modes | 2 | 50 | 55 | [] | [] | 24 | 11 |
| css/cssom-view | 2 | 50 | 55 | [] | [] | 82 | 44 |
| css/filter-effects | 2 | 50 | 55 | [] | [] | 25 | 12 |
| css/mediaqueries | 2 | 50 | 55 | [] | [] | 4 | 3 |
| css/selectors | 2 | 50 | 55 | [] | [] | 110 | 54 |
| dom | 2 | 35 | 35 | [] | [] | 240 | 84 |
| ecmascript | 2 | 35 | 35 | [] | [] | 29069 | 10391 |
| encrypted-media | 2 | 80 | 90 | [] | [] | 20 | 17 |
| fetch | 2 | 35 | 35 | [] | [] | 356 | 103 |
| fullscreen | 2 | 80 | 80 | [] | [] | 0 | 0 |
| hr-time | 2 | 50 | 50 | [] | [] | 9 | 4 |
| html | 2 | 0 | 20 | [] | [] | 1371 | 268 |
| media-capabilities | 2 | 50 | 50 | [] | [] | 0 | 0 |
| media-source | 2 | 90 | 95 | [] | [] | 4 | 4 |
| navigation-timing | 2 | 50 | 50 | [] | [] | 37 | 20 |
| notifications | 2 | 100 | 100 | [] | [] | 1 | 1 |
| page-visibility | 2 | 100 | 100 | [] | [] | 6 | 6 |
| performance-timeline | 2 | 50 | 50 | [] | [] | 41 | 9 |
| referrer-policy | 2 | 50 | 50 | [] | [] | 389 | 58 |
| resource-timing | 2 | 50 | 50 | [] | [] | 22 | 9 |
| service-workers | 2 | 100 | 100 | [] | [] | 8 | 8 |
| subresource-integrity | 2 | 100 | 100 | [] | [] | 1 | 1 |
| uievents | 2 | 100 | 100 | [] | [] | 8 | 8 |
| upgrade-insecure-requests | 2 | 55 | 55 | [] | [] | 62 | 36 |
| user-timing | 2 | 50 | 50 | [] | [] | 46 | 19 |
| webaudio | 2 | 15 | 35 | [] | [] | 145 | 49 |
| webgl | 2 | 0 | 25 | [] | [] | 82 | 18 |
| webmessaging | 2 | 35 | 35 | [] | [] | 68 | 16 |
| websockets | 2 | 35 | 35 | [] | [] | 80 | 29 |
| webstorage | 2 | 35 | 55 | [] | [] | 14 | 5 |
| workers | 2 | 35 | 35 | [] | [] | 128 | 36 |
| xhr | 2 | 35 | 65 | [] | [] | 126 | 60 |


