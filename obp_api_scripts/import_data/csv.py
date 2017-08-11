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

    def to_tribool(self, value):
        """
        Convert a given value to string triboolean as understood by the API
        Possible return values are 'true', 'false', '' or the actual value
        This method is prone to be changed as it seems the API's implementation
        does not work the way the author was told it would
        """
        if not value:
            return ''
        val = value.lower()
        if val == 'yes':
            return 'true'
        elif val == 'no':
            return 'false'
        else:
            # This is where we hopefully will never get to...
            return value

    def get_times(self, *data):
        times = {
            'monday': {
                'opening_time': data[0],
                'closing_time': data[1],
            },
            'tuesday': {
                'opening_time': data[2],
                'closing_time': data[3],
            },
            'wednesday': {
                'opening_time': data[4],
                'closing_time': data[5],
            },
            'thursday': {
                'opening_time': data[6],
                'closing_time': data[7],
            },
            'friday': {
                'opening_time': data[8],
                'closing_time': data[9],
            },
            'saturday': {
                'opening_time': data[10],
                'closing_time': data[11],
            },
            'sunday': {
                'opening_time': data[12],
                'closing_time': data[13],
            },
        }
        return times

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
                    LOGGER.info('Data to {} from CSV: {}'.format(self.method, data))
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
