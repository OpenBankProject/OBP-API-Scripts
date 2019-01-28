from requests_oauthlib import OAuth1Session
import json

import settings
from object.PostCounterparty import PostCounterparty
from object.User import User

if __name__ == "__main__":
    json_object_counterparty= PostCounterparty.load(settings.FILE_ROOT+"OBP_sandbox_counterparties_pretty.json")

    counterparty_list = [val for sublist in json_object_counterparty for val in sublist]

    json_object_user=User.load(settings.FILE_ROOT+"OBP_sandbox_pretty.json")

    for user_dict in json_object_user['users']:
        user = User(user_dict['user_name'], user_dict['password'], user_dict['email'])
        print("login as user: ")
        user.oauth_login()
        print("get users private accounts")
        private_account = user.get_user_private_account()
        account_list = json.loads(private_account)['accounts']
        print("ok!!!")

        session = OAuth1Session(
            settings.OAUTH_CONSUMER_KEY,
            settings.OAUTH_CONSUMER_SECRET,
            resource_owner_key=user.access_token,
            resource_owner_secret=user.access_secret,
        )
        print("get other accounts for the accounts")
        for account in account_list:
            bank_id = account['bank_id']
            region = bank_id.split('.')[2]
            account_id = account['id']
            view = account['views_available'][0]
            result = user.get_user_other_account(bank_id, account_id, view['id'])
            other_accounts_list = json.loads(result)['other_accounts']

            print("bank_id: {}".format(bank_id))

            print("region is {}".format(region))
            print("get matching json counterparty data for each transaction's other_account")
            for other_accounts in other_accounts_list:
                counterparty_name = other_accounts['holder']['name']
                print("Filtering counterparties by region {} and counterparty name {}".format(region, counterparty_name))
                regionCounterparties = [counterparty for counterparty in counterparty_list if counterparty['region']==region]
                records = [counterparty for counterparty in counterparty_list if counterparty['name'].lower()==counterparty_name.lower()]
                print("Found {} records".format(len(records)))
                for cp in records:
                    print("couterparty is Region {} Name {} Home Page {}".format(cp['region'],cp['name'],cp['homePageUrl']))
                    logoUrl = cp['homePageUrl'] if ("http://www.brandprofiles.com" in cp['logoUrl']) else cp['logoUrl']
                    if (logoUrl.startswith("http") and other_accounts['metadata']['image_URL'] is not None):
                        json = {"image_URL": logoUrl}
                        url = settings.API_HOST + "/obp/v3.1.0/banks/" + bank_id + "/accounts/" + account_id + "/" + view['id'] + "/other_accounts/"+other_accounts['id']+"/metadata/image_url"
                        result = session.request('POST', url, json = json, verify=False)
                        if result.status_code == 201:
                            print("saved " + logoUrl + " as imageURL for counterparty "+ other_accounts['id'])
                        else:
                            print("save failed")
                    else:
                        print("did NOT save " + logoUrl + " as imageURL for counterparty "+ other_accounts['id'])

                    if (cp['homePageUrl'].startswith("http") and not cp['homePageUrl'].endswith("jpg") and not cp['homePageUrl'].endswith("png") and other_accounts['metadata']['URL'] is not None):
                        json = {"URL": cp['homePageUrl']}
                        url = settings.API_HOST + "/obp/v3.1.0/banks/" + bank_id + "/accounts/" + account_id + "/" + \
                              view['id'] + "/other_accounts/" + other_accounts['id'] + "/metadata/url"
                        result = session.request('POST', url, json=json, verify=False)
                        if result.status_code == 201:
                            print("saved " + cp['homePageUrl'] + " as URL for counterparty "+ other_accounts['id'])
                        else:
                            print("save failed")
                    else:
                        print("did NOT save " + cp['homePageUrl'] + " as URL for counterparty "+ other_accounts['id'])

                    if (cp['category'] is not None and other_accounts['metadata']['more_info'] is not None):
                        categoryBits = cp['category'].split("_")
                        moreInfo = categoryBits[0]

                        json = {"more_info": moreInfo}
                        url = settings.API_HOST + "/v3.1.0/banks/" + bank_id + "/accounts/" + account_id + "/" + view['id'] + "/other_accounts/" + other_accounts['id'] + "/metadata/more_info"
                        result = session.request('POST', url, json=json, verify=False)
                        if result.status_code==201:
                            print("saved " + moreInfo + " as more_info for counterparty "+ other_accounts['id'])
                        else:
                            print("save failed")
                    else:
                        print("did NOT save more_info for counterparty "+ other_accounts['id'])

        user.oauth_logout()