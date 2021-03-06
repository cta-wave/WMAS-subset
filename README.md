# WMAS-subset
Subsets of the WMAS API specification for specific purposes including ATSC3.0/HbbTV usage. 

More: 
While the Web Media API Snapshot specification is appropriate for web media apps using HTML5/MSE/EME, there are other uses in which a subset of the API 
list can be helpful. One example is for ATSC3.0 Broadcast Apps ("BA's"), which are primariliy a JSON-based messaging app rather than a video player. However, 
such BA's still must draw themselves in the User Agent, still must use fonts and (many) other W3C APIs. This repo initially contains a WMAS subset for ATSC3.0 
and HbbTV (one subset covering both).


About Intellectual Property:
Any contribution made to the issues of this repository that results in a “shall” requirement pointing to an essential patent will require the company or individual 
holding the IPR to submit a Patent Holder Statement form. See https://standards.cta.tech/kwspub/rules/CTA-EP-23-T-IP-Proffer.pdf. Contributors are obliged to disclose to 
the working group any knowledge they may have of existing essential patents (or an intent to patent items whenever appropriate) affecting the work covered by this 
repository.

Note that CTA is not responsible for identifying any patents for which a license may be required by a CTA document, nor for conducting inquiries into the legal validity 
or scope of those patents that are brought to its attention. For further IPR information, see Section 15 of EP-23: 
https://standards.cta.tech/kwspub/rules/CTA-EP-23-T.pdf.

### Requirement

Python 3.6 or greater must be installed.
Install required packages:

```shell
pip install --upgrade pip
pip install -r requirements.txt
```

### Run subsetting script

To get creation date for all tests:

```shell
python get_test_creation_date.py
```

This script will clone wpt github repositry and checkout sepecific snapsot of WPT test directories for each testing group. Then reads the creation date of test files.
At the end of script it outputs a json file which contains creation date for all the tests.

To get subset of tests:

```shell
python subsetting_wpt.py
```

This script takes input parameters which defined in 'WMAS2019_input.json' and result from 'get_test_creation_date.py' and generates test subsets and
outputs a list of test subset in a json file.
