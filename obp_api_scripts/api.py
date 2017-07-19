# -*- coding: utf-8 -*-
#
# API module to handle the Open Bank Project API

import logging
import requests


LOGGER = logging.getLogger(__name__)


class APIError(Exception):
    """Exception class for API errors"""
    pass


class API(object):
    """OBP API Helper class"""
    def __init__(self, base_url, api_version):
        self.base_url = base_url
        self.api_url = '{}/obp/{}'.format(base_url, api_version)
        self.token = None

    def login(self, username, password, consumer_key):
        """Login to the API"""
        url = '{}/my/logins/direct'.format(self.base_url)
        fmt = 'DirectLogin username="{}",password="{}",consumer_key="{}"'
        headers = {
            'Authorization': fmt.format(username, password, consumer_key)
        }
        LOGGER.info('Login as {0} to {1}'.format(headers, url))
        response = requests.post(url, headers=headers)
        if (response.status_code != 200):
            raise APIError('Could not login: {}'.format(response.text))
        self.token = response.json()['token']
        LOGGER.debug('Received token: {0}'.format(self.token))
        return self.token

    def handle_response(self, response):
        """Handle the response, e.g. errors or conversion to JSON"""
        if response.status_code in [404, 500]:
            msg = '{}: {}'.format(response.status_code, response.text)
            raise APIError(msg)
        elif response.status_code in [204]:
            return response.text
        else:
            data = response.json()
            if 'error' in data:
                raise APIError(data['error'])
            return data

    def call(self, method='GET', urlpath='', data=None):
        """Actual call to the API"""
        url = '{}{}'.format(self.api_url, urlpath)
        headers = {
            'Authorization': 'DirectLogin token={}'.format(self.token),
            'Content-Type': 'application/json',
        }
        LOGGER.info('Calling API: {} {}'.format(method, url))
        response = requests.request(method, url, headers=headers, json=data)
        return self.handle_response(response)

    def get(self, urlpath=''):
        return self.call('GET', urlpath)

    def delete(self, urlpath):
        return self.call('DELETE', urlpath)

    def post(self, urlpath, data):
        return self.call('POST', urlpath, data)

    def put(self, urlpath, data):
        return self.call('PUT', urlpath, data)

    def get_current_user(self):
        """Convenience wrapper to get current user"""
        return self.get('/users/current')

