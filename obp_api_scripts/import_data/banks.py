# -*- coding: utf-8 -*-
#
# Import banks to the API


import sys

from .csv import ImportCSV


class ImportBanks(ImportCSV):
    args_num = 1
    args_usage = '<csv file>'

    def get_urlpath(self):
        urlpath = '/banks'
        return urlpath

    def get_data(self, row_number, row):
        data = {
            'id': row[0],
            'short_name': row[1],
            'full_name': row[2],
            'logo_url': '',
            'website_url': row[3],
            'swift_bic': '',
            'national_identifier': '',
            'bank_routing': {
                'scheme': '',
                'address': '',
            },
        }
        return data

