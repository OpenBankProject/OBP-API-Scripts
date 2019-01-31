import json
from requests_oauthlib import OAuth1Session
import re
import settings
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class User:
    def __init__(self, user_name, password, email=None):
        self.user_name = user_name
        self.password= password
        self.email = email

    @staticmethod
    def load(path):
        with open(path, encoding="utf-8") as file:
            file_content = file.read()
        json_object = json.loads(file_content)
        return json_object

    def oauth_login(self):
        session = OAuth1Session(
            settings.OAUTH_CONSUMER_KEY,
            client_secret=settings.OAUTH_CONSUMER_SECRET,
            callback_uri=settings.LOGIN_AGENT_URL +settings.OAUTH_AUTHORIZATION_PATH,
        )

        url = settings.API_HOST + settings.OAUTH_TOKEN_PATH
        response = session.fetch_request_token(url, verify=False)

        self.oauth_token = response.get('oauth_token')
        self.oauth_secret = response.get('oauth_token_secret')

        url = settings.API_HOST + settings.OAUTH_AUTHORIZATION_PATH
        authorization_url = session.authorization_url(url)

        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.get(authorization_url)
        username_element = driver.find_element_by_name("username")
        username_element.send_keys(self.user_name)
        password_element = driver.find_element_by_name("password")
        password_element.send_keys(self.password)
        submit_button = driver.find_element_by_class_name("submit")
        submit_button.click()
        current_url = driver.current_url
        print(current_url)
        driver.close()
        p = re.compile(".*?oauth_token=(.*)&oauth_verifier=(.*)")
        result = p.search(current_url)
        try:
            self.oauth_verifier = result.group(2)
        except:
            print("login failed!!!")
            return None

        print("oauth_token: {}\noauth_secret: {}".format(self.oauth_token, self.oauth_secret))

        self.session = OAuth1Session(
            settings.OAUTH_CONSUMER_KEY,
            settings.OAUTH_CONSUMER_SECRET,
            resource_owner_key=self.oauth_token,
            resource_owner_secret=self.oauth_secret,
            verifier=self.oauth_verifier
        )
        self.session.parse_authorization_response(authorization_url)
        url = settings.API_HOST + settings.OAUTH_ACCESS_TOKEN_PATH
        response = self.session.fetch_access_token(url)
        self.access_token = response.get('oauth_token')
        self.access_secret = response.get('oauth_token_secret')
        print("access_token: {}\naccess_secret: {}".format(self.access_token, self.access_secret))

        return self.session

    def get_user_private_account(self):

        result = self.session.get(settings.API_HOST+"/obp/v1.2.1/accounts/private")
        if result.status_code==200:
            return result.content
        else:
            return '{"accounts":[]}'

    def get_user_other_account(self, bank_id, account_id, view_id):

        session = OAuth1Session(
            settings.OAUTH_CONSUMER_KEY,
            settings.OAUTH_CONSUMER_SECRET,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_secret,
        )
        result = session.get(
            settings.API_HOST+"/obp/v3.1.0/banks/"+bank_id+"/accounts/"+account_id+"/"+view_id+"/other_accounts")

        if result.status_code==200:
            return result.content
        else:
            return []

    def __str__(self):
        return self.user_name+"\t"+self.email

    def oauth_logout(self):
        pass