# -*- coding: utf-8 -*-
#
# Import products to given bank_id


from .csv import ImportCSV


class ImportProducts(ImportCSV):
    method = 'PUT'
    args_num = 2
    args_usage = '<csv file> <bank_id>'

    def get_urlpath(self):
        urlpath = '/banks/{}/products'.format(self.bank_id)
        return urlpath

    def get_data(self, row_number, row):
        data = {
            'bank_id': self.bank_id,
            'code': row[0],
            'name': row[1],
            'category': row[2],
            'family': row[3],
            'super_family': row[4],
            'more_info_url': row[5],
            'details': row[6],
            'description': '',
            'meta': {
                'license': {
                    'id': 'copyright',
                    'name': 'Copyright 2017',
                }
            }
        }
        return data
