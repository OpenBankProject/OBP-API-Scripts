# -*- coding: utf-8 -*-
#
# Format of input JSON file:
# [
#    {
#        "username": "",
#        "password": "",
#        "consumer_key": "",
#    }
# ]


import json
import logging
from pprint import pprint

from ..api import API, APIError
from settings import BASE_URL, API_VERSION


LOGGER = logging.getLogger(__name__)


class PrintAccountDataError(Exception):
    """Exception class for PrintAccountData"""
    pass


class PrintAccountData(object):
    def __init__(self, args):
        if len(args) < 2:
            msg = 'Usage: {} <json file>'.format(args[0])
            raise PrintAccountDataError(msg)
        self.filename_logins = args[1]

    def print_transactions(self, api, account):
        urlpath = '/banks/{}/accounts/{}/{}/transactions'.format(
            account['bank_id'], account['id'], 'owner')
        transactions = api.get(urlpath)
        if 'transactions' in transactions:
            transactions = transactions['transactions']
        print('Number of transactions: {}'.format(len(transactions)))

    def print_accounts(self, username, api):
        print('')
        print('------')
        print('Accounts for username {} at {}:'.format(username, api.base_url))
        accounts = api.get('/my/accounts')
        for account in accounts:
            pprint(account)
            self.print_transactions(api, account)
            print('---')
        print('')

    def run(self):
        logins = json.loads(open(self.filename_logins).read())
        for login in logins:
            api = API(BASE_URL, API_VERSION)
            try:
                api.login(login['username'],
                          login['password'],
                          login['consumer_key'])
                self.print_accounts(login['username'], api)
            except APIError as err:
                LOGGER.info(str(err))

