# A collection of scripts dealing with the API

All these are using DirectLogin


## Setup

- Create a virtual environment: `virtualenv --python=python3 venv`
- Then activate it: `source venv/bin/activate`
- Now install requests in the virtualenv: `pip install -r requirements.txt`
- Copy `settings.py.example` to `settings.py` and edit to suit your needs.

- For future runs, you need to activate the virtualenv again, but do not need to recreate it or install the requirements.
- When you are done, `deactivate` the virtualenv


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
