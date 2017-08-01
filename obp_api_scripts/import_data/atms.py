# -*- coding: utf-8 -*-
#
# Import ATMs to the API


from .csv import ImportCSV


class ImportATMs(ImportCSV):
    args_num = 2
    args_usage = '<csv file> <bank_id>'

    def get_urlpath(self):
        urlpath = '/banks/{}/atms'.format(self.bank_id)
        return urlpath

    def get_data(self, row_number, row):
        data = {
            'bank_id': row[0],
            'id': row[1],
            'name': row[2],
            'address': {
                'line_1': row[3],
                'line_2': row[4],
                'line_3': row[5],
                'city': row[7] if not row[6] else row[6],
                'state': row[8],
                'postcode': row[9],
                'country': row[10],
            },
            'location': {
                'latitude': float(row[11]) if row[11] else 0,
                'longitude': float(row[12]) if row[12] else 0,
            },
            'meta': {
                'license': {
                    'id': 'copyright',
                    'name': 'Copyright 2017',
                },
            },
        }
        return data
