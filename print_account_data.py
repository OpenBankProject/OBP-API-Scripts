#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This script prints all accounts and the number of transactions for each of
# them. The accounts to query are defined by a JSON file which contains
# username, password and consumer key.
#
# Format of input JSON file:
# [
#    {
#        "username": "",
#        "password": "",
#        "consumer_key": "",
#    }
# ]
#
# Example usage: ./print_account_data.py logins.json
#

import sys

from obp_api_scripts.print_data.accounts import PrintAccountData


PrintAccountData(sys.argv).run()
