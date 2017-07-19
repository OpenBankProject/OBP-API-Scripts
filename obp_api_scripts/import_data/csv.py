# -*- coding: utf-8 -*-
#
# Module with base class for importing from CSV files


import csv
import logging

from settings import (
    BASE_URL, API_VERSION, USERNAME, PASSWORD, CONSUMER_KEY)
from ..api import API


LOGGER = logging.getLogger(__name__)


class ImportCSVError(Exception):
    """Exception class for Importer errors"""
    pass


class ImportCSV(object):
    """
    Convert a CSV file into a format to be posted to the OBP API
    This is a base class for importer scripts to specialise
    """

    # HTTP method to use to import data
    method = 'POST'
    # Number of arguments to the script using the importer class
    args_num = 0
    # Usge string printed for arguments if args_num is not satisfied
    args_usage = None
    # Default filename
    filename = None
    # Default bank id
    bank_id = None

    def __init__(self, args):
        if len(args) < self.args_num + 1:
            msg = 'Usage: {} {}'.format(args[0], self.args_usage)
            raise ImportCSVError(msg)
        if self.args_num > 0:
            self.filename = args[1]
        if self.args_num > 1:
            self.bank_id = args[2]

    def run(self):
        """
        Do the actual work by reading the CSV file and sending data to API
        """
        api = API(BASE_URL, API_VERSION)
        if api.login(USERNAME, PASSWORD, CONSUMER_KEY):
            with open(self.filename, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)  # skip header
                row_number = 0
                for row in reader:
                    data = self.get_data(row_number, row)
                    LOGGER.info('Got data: {}'.format(data))
                    api.call(self.method, self.get_urlpath(), data)
                    row_number += 1

    def get_urlpath(self, row):
        """
        Define URL path to POST to API
        This must be implemented by child class!
        """
        raise(NotImplementedError)

    def get_data(self, row_number, row):
        """
        Define data to POST to API
        This must be implemented by child class!
        """
        raise(NotImplementedError)

