import settings
from object.Bank import Bank
from object.PostCustomer import PostCustomer
from object.User import User
import json

if __name__ == "__main__":
    adminUserUsername = settings.ADMIN_USERNAME
    adminPassword = settings.ADMIN_PASSWORD

    json_customers = PostCustomer.load(settings.FILE_ROOT+"OBP_sandbox_customers_pretty.json")

    print("Got {} records".format(len(json_customers)))

    customer_list = [PostCustomer(customer['customer_number'],
                                  customer['legal_name'],
                                  customer['mobile_phone_number'],
                                  customer['email'],
                                  customer['face_image'],
                                  customer['date_of_birth'],
                                  customer['relationship_status'],
                                  customer['dependants'],
                                  customer['dob_of_dependants'],
                                  customer['highest_education_attained'],
                                  customer['employment_status'],
                                  customer['kyc_status'],
                                  customer['last_ok_date'],
                                  customer['bank_id'],
                                  customer['credit_rating'],
                                  customer['credit_limit']
                                 ) for customer in json_customers]

    json_user = User.load(settings.FILE_ROOT+"OBP_sandbox_pretty.json")
    print("Got {} users".format(len(json_user['users'])))

    print("login as user: ")
    admin_user = User(adminUserUsername, adminPassword)
    session = admin_user.oauth_login()
    print("ok!!!")

    print("Got {} banks".format(len(json_user['banks'])))
    bank_list=[]
    for bank in json_user['banks']:
        bank_list.append(Bank(bank['id'],
                              bank['short_name'],
                              bank['full_name'],
                              bank['logo'],
                              bank['website']))

    for user_dict in json_user['users']:
        user = User(user_dict['user_name'], user_dict['password'], user_dict['email'])
        customer_filtered = [customer for customer in customer_list if customer.email == user.email]
        result = session.get(
            settings.API_HOST + "/obp/v3.1.0/users/username/" + user.user_name)
        if result.status_code==200:
            current_user = json.loads(result.content)

            for customer in customer_filtered:
                print("email is {} customer number is {} name is {} and has {} dependants born on {} "
                    .format(customer.email, customer.customer_number, customer.legal_name, customer.dependants, customer.dob_of_dependants))

                for bank in bank_list:
                    print("Posting a customer for bank {}".format(bank.short_name))
                    url = settings.API_HOST+"/obp/v3.1.0/banks/{}/customers".format(bank.id)
                    result2 = session.request('POST', url, json=customer.to_json(current_user['user_id']), verify=False)
                    if result2.status_code==201:
                        print("saved {} as customer {}".format(customer.customer_number, result2.content))
                    else:
                        print("did NOT save customer {}".format(result2.error))
