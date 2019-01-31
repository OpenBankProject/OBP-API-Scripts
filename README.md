# A collection of scripts dealing with the API

All these are using DirectLogin


## Setup

- Create a virtual environment: `virtualenv --python=python3 venv`
- Then activate it: `source venv/bin/activate`
- Now install requests in the virtualenv: `pip install -r requirements.txt`
- Copy `settings.py.example` to `settings.py` and edit to suit your needs.

- For future runs, you need to activate the virtualenv again, but do not need to recreate it or install the requirements.
- When you are done, `deactivate` the virtualenv


## Example input

- In directory `example_input` you will find CSV/JSON files which should explain the format the scripts expect the input data to be.


## Import Data

Python scripts to import data into the API

- `./import_banks.py <csv file>`
- `./import_branches.py <csv file> <bank id>`
- `./import_products.py <csv file> <bank id>`
- `./import_atms.py <csv file> <bank id>`


You probably have to edit the importer classes (method `get_data`) to match your input data as this changes with every dataset.



## Print Data

- `./print_account_data.py <json file>`


## Generate statistics

This is a bit different as it does not use the API, but talks directly to the database used by the API. You need to configure the settings accordingly. Run it _on the database server_ with `./generate_stats.py`

the webdriver of firefox or chrome need to be installed for selenium.
  
## Start services
Please make sure that OBP-API server and API-Tester server is running

## Configure settings

Create and edit `settings.py`, this setting file is used mainly for oauth1.0 login(both users and admin):

```python

#Consumer key + secret to authenticate the _app_ against the API
OAUTH_CONSUMER_KEY = '<key>'
OAUTH_CONSUMER_SECRET = '<secret>'
# API hostname, e.g. https://api.openbankproject.com
API_HOST = '<hostname>'

# API_VERSION Used in project
API_VERSION = '3.1.0'

# API Tester hostname, e.g. https://apitester.openbankproject.com
LOGIN_AGENT_URL = 'http://127.0.0.1:9090'

OAUTH_TOKEN_PATH = '/oauth/initiate'
OAUTH_AUTHORIZATION_PATH = '/oauth/authorize'
OAUTH_ACCESS_TOKEN_PATH = '/oauth/token'

# Admin username and password
ADMIN_USERNAME = '<username>'
ADMIN_PASSWORD = '<password>'

FILE_ROOT = '<path>'
```

## run PostCounterparty.py

```bash
$ python OBP\run\PostCounterpartyScript.py
```

## run PostCustomer.py

make sure your admin account have the roles below: 
CanCreateCustomer or CanCreateCustomerAtAnyBank
```bash
$ python OBP\run\PostCustomerScript.py
```