# -*- coding: utf-8 -*-

# Answer a few questions about statistics not easily possible using SQL only


import datetime
import psycopg2
import statistics

from settings import (
    ACTIVE_APPS_DATE_START,
    APPNAME_APIEXPLORER,
    DATABASE,
    DATE_START, DATE_END,
    EXCLUDE_APPS, EXCLUDE_FUNCTIONS, EXCLUDE_URL_PATTERN,
    SERVER_TIMEZONE
)


DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
SQL_DATE_RANGE_FORMAT = "date_c >= to_timestamp('{}', 'yyyy-mm-dd hh24:mi:ss') AND date_c <= to_timestamp('{}', 'yyyy-mm-dd hh24:mi:ss')"  # noqa


def pretty_decoration(function):
    """
    Puts some pretty decoration around a function call
    """
    def wrapper(*args, **kwargs):
        print('-' * 78)
        result = function(*args, **kwargs)
        print('-' * 78)
        print('\n')
        return result
    return wrapper


class Stats(object):
    """
    Calculate statistics about the usage of a sandbox
    """

    def __init__(self):
        self.date_start = DATE_START
        self.date_end = DATE_END
        self.results = {}
        self.sql = {
            'date_range': SQL_DATE_RANGE_FORMAT.format(
                self.date_start, self.date_end),
            'exclude_apps': "appname NOT IN ('')",
            'exclude_functions': "implementedbypartialfunction NOT IN ('')",
            'exclude_url_pattern': "url NOT LIKE ''",
        }
        if EXCLUDE_APPS:
            wrapped = map(lambda x: "'{}'".format(x), EXCLUDE_APPS)
            self.sql['exclude_apps'] = 'appname NOT IN ({})'.format(
                ', '.join(wrapped))
        if EXCLUDE_FUNCTIONS:
            wrapped = map(lambda x: "'{}'".format(x), EXCLUDE_FUNCTIONS)
            self.sql['exclude_functions'] = 'implementedbypartialfunction NOT IN ({})'.format(  # noqa
                ', '.join(wrapped))
        if EXCLUDE_URL_PATTERN:
            self.sql['exclude_url_pattern'] = "url NOT LIKE '{}'".format(
                EXCLUDE_URL_PATTERN)

        connstring = "host='{}' dbname='{}' user='{}' password='{}'"
        self.connection = psycopg2.connect(connstring.format(
            DATABASE['host'],
            DATABASE['name'],
            DATABASE['user'],
            DATABASE['password']))
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Properly clean up connection resources
        """
        self.cursor.close()
        self.connection.close()

    @pretty_decoration
    def total_calls(self):
        """
        Prints how many calls were made in total
        """
        query = 'SELECT COUNT(*) FROM mappedmetric WHERE {} AND {} AND {} AND {};'.format(  # noqa
            self.sql['date_range'],
            self.sql['exclude_apps'],
            self.sql['exclude_functions'],
            self.sql['exclude_url_pattern'],
        )
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        self.results['total_calls'] = result[0]
        print('Total calls: {}'.format(self.results['total_calls']))

    @pretty_decoration
    def total_calls_apiexplorer(self):
        """
        Prints how many calls were made using the API Explorer
        """
        query = "SELECT COUNT(*) FROM mappedmetric WHERE {} AND {} AND {} AND appname = '{}';".format(  # noqa
            self.sql['date_range'],
            self.sql['exclude_functions'],
            self.sql['exclude_url_pattern'],
            APPNAME_APIEXPLORER,
        )
        self.cursor.execute(query)
        calls = self.cursor.fetchone()[0]
        percentage = 100
        if 'total_calls' in self.results:
            percentage = round(calls * 100 / self.results['total_calls'])
        print('Total authenticated calls using API Explorer: {} ({}%)'.format(
            calls, percentage))

    @pretty_decoration
    def total_calls_pre_v300(self):
        """
        Prints how many calls were made using a version prior to v3.0.0
        v3.0.0 is the 'good' version where things are logged properly.
        Many of your SDKs and apps still use old version, though.
        """
        query = "SELECT COUNT(*) FROM mappedmetric WHERE {} AND {} AND {} AND {} AND implementedinversion < 'v3.0.0';".format(  # noqa
            self.sql['date_range'],
            self.sql['exclude_apps'],
            self.sql['exclude_functions'],
            self.sql['exclude_url_pattern'],
        )
        self.cursor.execute(query)
        calls = self.cursor.fetchone()[0]
        percentage = 100
        if 'total_calls' in self.results:
            percentage = round(calls * 100 / self.results['total_calls'])
        print('Total calls using version < v3.0.0: {} ({}%)'.format(
            calls, percentage))

    @pretty_decoration
    def apps(self):
        """
        Prints number of apps with distinct developer email addresses
        """
        query_fmt = "SELECT COUNT(DISTINCT name) FROM consumer WHERE name <> '' AND {};"  # noqa
        exclude_apps = self.sql['exclude_apps'].replace('appname', 'name')
        query = query_fmt.format(exclude_apps)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        print('Number of apps with distinct names: {}'.format(result[0]))

        query = query.replace(
            'COUNT(DISTINCT name)',
            'COUNT(DISTINCT developeremail)')
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        msg = 'Number of apps with distinct developer email addresses: {}'
        print(msg.format(result[0]))

    @pretty_decoration
    def app_names(self):
        """
        Prints app names
        """
        query_fmt = "SELECT DISTINCT name FROM consumer WHERE name <> '' AND {};"  # noqa
        exclude_apps = self.sql['exclude_apps'].replace('appname', 'name')
        query = query_fmt.format(exclude_apps)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        names = sorted(map(lambda x: x[0], result))
        print('{} app names: {}'.format(len(names), names))

    @pretty_decoration
    def active_apps(self):
        """
        Prints the names of apps using the API after a certain date
        """
        query = "SELECT DISTINCT appname FROM mappedmetric WHERE date_c >= to_timestamp('{}', 'yyyy-mm-dd hh24:mi:ss') AND {} AND {} AND {};".format(  # noqa
            ACTIVE_APPS_DATE_START,
            self.sql['exclude_apps'],
            self.sql['exclude_functions'],
            self.sql['exclude_url_pattern'],
        )
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        names = sorted(map(lambda x: x[0], result))
        print('{} apps used after {}: {}'.format(
            len(names), ACTIVE_APPS_DATE_START, names))

    @pretty_decoration
    def avg_number_of_calls_per_day(self):
        """
        Prints average number of calls per day
        """
        date_start = datetime.datetime.strptime(self.date_start, DATE_FORMAT)
        date_end = datetime.datetime.strptime(self.date_end, DATE_FORMAT)
        number_of_days = (date_end - date_start).days
        query = "SELECT (SELECT COUNT(*) FROM mappedmetric WHERE {} AND {} AND {} AND {}) / {};".format(  # noqa
            self.sql['date_range'],
            self.sql['exclude_apps'],
            self.sql['exclude_functions'],
            self.sql['exclude_url_pattern'],
            number_of_days,
        )
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        print('Avg number of calls per day: {}'.format(result[0]))

    @pretty_decoration
    def avg_response_time(self):
        """
        Prints average response time
        """
        query = 'SELECT AVG(duration) FROM mappedmetric WHERE {} AND {} AND {} AND {};'.format(  # noqa
            self.sql['date_range'],
            self.sql['exclude_apps'],
            self.sql['exclude_functions'],
            self.sql['exclude_url_pattern'],
        )
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        response_time = int(round(result[0]))
        print('Avg response time: {} ms'.format(response_time))

    @pretty_decoration
    def most_used_api_calls(self, limit):
        """
        Prints most used API calls
        """
        query = "SELECT verb, url, implementedbypartialfunction, COUNT(*) AS count FROM mappedmetric WHERE {} AND {} AND {} AND {} GROUP BY verb, url, implementedbypartialfunction ORDER BY count DESC LIMIT {};".format(  # noqa
            self.sql['date_range'],
            self.sql['exclude_apps'],
            self.sql['exclude_functions'],
            self.sql['exclude_url_pattern'],
            limit,
        )
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        print('{} most used API calls:'.format(limit))
        for call in result:
            out = call[2] if call[2] else call[1]
            print('{} {}: {}'.format(call[0], out, call[3]))

    @pretty_decoration
    def most_used_warehouse_calls(self, limit):
        """
        Prints most used warehouse API calls
        """
        # Since elasticSearchWarehouseV300 was introduced in ca. June 2017
        # the URL does not contain parameters anymore. We cannot access the
        # payload from the POST and hence do not know how ES was actually
        # used.
        query = "SELECT url, COUNT(*) AS count FROM mappedmetric WHERE implementedbypartialfunction LIKE 'elasticSearchWarehouse%' AND {} AND {} AND {} AND {} GROUP BY url ORDER BY count DESC LIMIT {};".format(  # noqa
            self.sql['date_range'],
            self.sql['exclude_apps'],
            self.sql['exclude_functions'],
            self.sql['exclude_url_pattern'],
            limit,
        )
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        print('{} most used Warehouse calls:'.format(limit))
        for call in result:
            print('{}: {}'.format(call[0], call[1]))

    @pretty_decoration
    def top_apps_using_warehouse(self, limit):
        """
        Prints the top apps using the Elasticsearch warehouse
        """
        query = "SELECT mappedmetric.appname as appname, consumer.developeremail as email, consumer.description as description, COUNT(*) AS count FROM mappedmetric, consumer WHERE mappedmetric.appname = consumer.name AND mappedmetric.implementedbypartialfunction LIKE 'elasticSearchWarehouse%' AND {} AND {} AND {} AND {} GROUP BY appname, email, description ORDER BY count DESC LIMIT {};".format(  # noqa
            self.sql['date_range'],
            self.sql['exclude_apps'],
            self.sql['exclude_functions'],
            self.sql['exclude_url_pattern'],
            limit,
        )
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        print('{} top apps using the Warehouse:'.format(limit))
        for call in result:
            print('{} / {}: {}\n{}\n'.format(call[0], call[1], call[3], call[2]))

    @pretty_decoration
    def users_with_CanSearchWarehouse(self):
        """
        Prints the users and their total number with access to the warehouse
        """
        query = "SELECT DISTINCT resourceuser.name_, resourceuser.email FROM resourceuser, mappedentitlement WHERE mappedentitlement.mrolename = 'CanSearchWarehouse' AND mappedentitlement.muserid = resourceuser.userid_ ORDER BY resourceuser.name_"  # noqa
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        print('Users with role CanSearchWarehouse:')
        for user in result:
            print('{} ({})'.format(user[0], user[1]))
        print('Total users with role CanSearchWarehouse: {}'.format(
            len(result)))

    @pretty_decoration
    def median_time_from_consumer_registration_to_first_api_call(self):
        """
        Prints average time from consumer registration to first API call
        """
        # Only during hackathon:
        sql_date_range_createdat = self.sql['date_range'].replace(
            'date_c', 'createdat')
        query = "SELECT createdat, id FROM consumer WHERE {};".format(
                sql_date_range_createdat)
        # At all times:
        # query = "select createdat, id from consumer;"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        times_to_first_call = []
        for consumer in result:
            query = 'SELECT date_c FROM mappedmetric WHERE {} AND {} AND {} AND {} AND consumerid = cast({} AS VARCHAR) ORDER BY date_c DESC LIMIT 1;'.format(  # noqa
                self.sql['date_range'],
                self.sql['exclude_apps'],
                self.sql['exclude_functions'],
                self.sql['exclude_url_pattern'],
                consumer[1],
            )
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            if result:
                time_to_first_call = result[0] - consumer[0]
                print('Time to first call for consumer {}: {}'.format(
                    consumer[1], time_to_first_call))
                times_to_first_call.append(time_to_first_call.total_seconds())
        median = statistics.median(times_to_first_call)
        delta = datetime.timedelta(seconds=median)
        msg = 'Median time from consumer registration to first API call: {}'
        print(msg.format(delta))

    @pretty_decoration
    def most_diverse_usage(self, limit):
        """
        Prints most diverse usage of API calls by developer email address
        """
        # Naively adding consumer.id to SELECT will change ranking if some
        # people use same email addressfor different consumers
        query = "SELECT COUNT(DISTINCT mappedmetric.implementedbypartialfunction) AS count, consumer.developeremail FROM mappedmetric, consumer WHERE mappedmetric.implementedbypartialfunction <> '' AND {} AND {} AND {} AND {} AND mappedmetric.consumerid = CAST(consumer.id AS character varying) GROUP BY consumer.developeremail ORDER BY count DESC LIMIT {};".format(  # noqa
            self.sql['date_range'],
            self.sql['exclude_apps'],
            self.sql['exclude_functions'],
            self.sql['exclude_url_pattern'],
            limit,
        )
        self.cursor.execute(query)
        top_callers = self.cursor.fetchall()
        msg = '{} most diverse usage of API calls by developer email address:'
        print(msg.format(limit))
        for caller in top_callers:
            query = "SELECT DISTINCT mappedmetric.implementedbypartialfunction FROM mappedmetric, consumer WHERE mappedmetric.implementedbypartialfunction <> '' AND mappedmetric.consumerid = CAST(consumer.id AS character varying) AND consumer.developeremail = '{}' AND {} AND {} AND {} AND {}".format(  # noqa
                caller[1],
                self.sql['date_range'],
                self.sql['exclude_apps'],
                self.sql['exclude_functions'],
                self.sql['exclude_url_pattern'],
            )
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            calls = map(lambda x: x[0], result)
            msg = '{}: {}\n\tCalls: {}'
            print(msg.format(caller[0], caller[1], ', '.join(calls)))

    def calls_per_delta(self, **delta):
        """
        Prints how many calls were made in total per given delta
        """
        query_fmt = 'SELECT COUNT(*) FROM mappedmetric WHERE {} AND {} AND {} AND {};'  # noqa
        query_fmt = query_fmt.format(
            SQL_DATE_RANGE_FORMAT,
            self.sql['exclude_apps'],
            self.sql['exclude_functions'],
            self.sql['exclude_url_pattern'],
        )
        date_start = datetime.datetime.strptime(self.date_start, DATE_FORMAT)
        date_end = datetime.datetime.strptime(self.date_end, DATE_FORMAT)
        date_from = date_start
        date_to = date_start + datetime.timedelta(**delta)
        sum = 0
        while date_to <= date_end:
            query = query_fmt.format(date_from, date_to)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            print('{} - {} # {}'.format(
                date_from, date_to, result[0]))
            sum += result[0]
            date_from = date_to
            date_to = date_to + datetime.timedelta(**delta)
        print('Sanity check: {} calls'.format(sum))

    @pretty_decoration
    def calls_per_month(self):
        """
        Convenience function to print number of calls per month
        It is actually 30 days, not a month
        """
        print('Calls per Month (Server timezone is {}):'.format(SERVER_TIMEZONE))
        self.calls_per_delta(days=30)

    @pretty_decoration
    def calls_per_day(self):
        """
        Convenience function to print number of calls per day
        """
        print('Calls per Day (Server timezone is {}):'.format(SERVER_TIMEZONE))
        self.calls_per_delta(days=1)

    @pretty_decoration
    def calls_per_half_day(self):
        """
        Convenience function to print number of calls per half day
        """
        msg = 'Calls per Half Day (Server timezone is {}):'
        print(msg.format(SERVER_TIMEZONE))
        self.calls_per_delta(hours=12)

    @pretty_decoration
    def calls_per_hour(self):
        """
        Convenience function to print number of calls per hour
        """
        msg = 'Calls per Hour (Server timezone is {}):'
        print(msg.format(SERVER_TIMEZONE))
        self.calls_per_delta(hours=1)

    def run_all(self):
        self.total_calls()
        self.total_calls_apiexplorer()
        self.total_calls_pre_v300()
        self.calls_per_month()
        self.calls_per_day()
        self.calls_per_half_day()
        self.calls_per_hour()
        self.apps()
        self.app_names()
        self.active_apps()
        self.avg_number_of_calls_per_day()
        self.avg_response_time()
        self.most_used_api_calls(30)
        self.most_used_warehouse_calls(10)
        self.top_apps_using_warehouse(10)
        self.users_with_CanSearchWarehouse()
        self.median_time_from_consumer_registration_to_first_api_call()
        self.most_diverse_usage(5)
