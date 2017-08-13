# -*- coding: utf-8 -*-
#
# Import ATMs to the API


from .csv import ImportCSV
from settings import LICENSE


class ImportATMs(ImportCSV):
    args_num = 2
    args_usage = '<csv file> <bank_id>'

    def get_urlpath(self):
        urlpath = '/banks/{}/atms'.format(self.bank_id)
        return urlpath

    def get_data(self, row_number, row):
        self.check_bank_id(row_number, row)
        data = {
            'bank_id': row[0],
            'id': row[1],
            'name': row[2],
            'address': {
                'line_1': row[3],
                'line_2': row[4],
                'line_3': row[5],
                'city': row[7] if not row[6] else row[6],
                'county': '',
                'state': row[8],
                'postcode': row[9],
                'country_code': row[10],
            },
            'location': {
                'latitude': float(row[11]) if row[11] else 0,
                'longitude': float(row[12]) if row[12] else 0,
            },
            'meta': {
                'license': LICENSE,
            },
            'located_at': row[13],
            #'has_deposit_capability': self.to_tribool(row[14]),
            # Hard-code to false for the time being:
            'has_deposit_capability': 'false',
            'is_accessible': self.to_tribool(row[15]),
            'more_info': '',
        }
        data.update(self.get_times(
            row[16], row[17], row[18], row[19], row[20], row[21], row[22],
            row[23], row[24], row[25], row[26], row[27], row[28], row[29],
        ))
        return data
