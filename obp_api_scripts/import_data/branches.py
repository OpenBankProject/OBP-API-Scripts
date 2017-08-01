# -*- coding: utf-8 -*-
#
# Import branches to given bank id


from .csv import ImportCSV


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
                'city': row[6],
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
                }
            },
            'lobby': {
                'hours': self.get_hours(row, 16),
            },
            'drive_up': {
                'hours': self.get_hours(row, 30),
            },
            'branch_routing': {
                'scheme': '',
                'address': '',
            }
        }
        return data
