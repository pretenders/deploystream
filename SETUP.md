# Set up environment to run tests

## Install dependencies

OS-level dependencies, use whatever install procedure works on your OS:
* `curl` (for `nodeenv`)
* `chrome` (the Google browser, for `testacular`)

* Make yourself a virtual environment, and activate it
* Install python packages with `pip install -r requirements/test.txt`
* Make yourself a node environment within the virtualenv with `nodeenv -p`
  (this installs node and npm and takes quite a while)
* Install node packages with `scripts/nodereqs.py`
  (this installs the required files listed in `requirements/nodeenv.txt`)

## Run the tests

* Angular Unit tests: `scripts/angular-unit-test.sh`
* Angular E2E tests: `scripts/angular-e2e-test.sh` (requires a running server)
* Python tests: `nosetests`
