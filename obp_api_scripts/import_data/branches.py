# -*- coding: utf-8 -*-
#
# Import branches to given bank id


from .csv import ImportCSV
from settings import LICENSE


class ImportBranches(ImportCSV):
    args_num = 2
    args_usage = '<csv file> <bank_id>'

    def get_urlpath(self):
        urlpath = '/banks/{}/branches'.format(self.bank_id)
        return urlpath

    def get_hours(self, row, idx_start):
        hours = []
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        idx = idx_start
        for day in days:
            today = ''
            if row[idx]:
                today += '{}: {}'.format(day, row[idx])
            if row[idx+1]:
                today += ' - {}'.format(row[idx+1])
            if today:
                hours.append(today)
            idx += 2
        hours = ', '.join(hours)
        return hours

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
                'county': '',
                'state': row[8],
                'postcode': row[9],
                'country_code': row[10],
            },
            'location': {
                'latitude': float(row[11]) if row[11] else 0,
                'longitude': float(row[12]) if row[12] else 0,
            },
            'phone_number': row[13],
            'is_accessible': '',
            #'is_accessible': self.to_tribool(row[XXX]),
            'branch_type': row[14],
            'more_info': row[15],
            'lobby': self.get_times(
                row[16], row[17], row[18], row[19], row[20], row[21], row[22],
                row[23], row[24], row[25], row[26], row[27], row[28], row[29],
            ),
            'drive_up': self.get_times(
                row[30], row[31], row[32], row[33], row[34], row[35], row[36],
                row[37], row[38], row[39], row[40], row[41], row[42], row[43],
            ),
            'meta': {
               'license': LICENSE,
            },
            'branch_routing': {
               'scheme': '',
               'address': '',
            }
        }
        return data
