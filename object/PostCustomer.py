import json


class PostCustomer:
    def __init__(self, customer_number, legal_name,
                 mobile_phone_number, email, face_image,
                 date_of_birth, relationship_status, dependants,
                 dob_of_dependants, highest_education_attained,
                 employment_status, kyc_status, last_ok_date,
                 bank_id, credit_rating, credit_limit):
        self.customer_number = customer_number
        self.legal_name= legal_name
        self.mobile_phone_number = mobile_phone_number
        self.email = email
        self.face_image = face_image
        self.date_of_birth = date_of_birth
        self.relationship_status = relationship_status
        self.dependants = dependants
        self.dob_of_dependants = dob_of_dependants
        self.highest_education_attained = highest_education_attained
        self.employment_status = employment_status
        self.kyc_status = kyc_status
        self.last_ok_date = last_ok_date
        self.bank_id = bank_id
        self.credit_rating = credit_rating
        self.credit_limit = credit_limit

    @staticmethod
    def load(path):
        with open(path, encoding="utf-8") as file:
            file_content = file.read()
        json_object = json.loads(file_content)
        return json_object

    def __str__(self):
        return self.legal_name+"\t"+self.email

    def to_json(self, user_id):
        return {
            "user_id":user_id,
            "customer_number":self.customer_number,
            "legal_name": self.legal_name,
            "mobile_phone_number": self.mobile_phone_number,
            "email": self.email,
            "face_image": self.face_image,
            "date_of_birth": self.date_of_birth,
            "relationship_status": self.relationship_status,
            "dependants": self.dependants,
            "dob_of_dependants": self.dob_of_dependants,
            "credit_rating": {
                "rating": "A",
                "source": "Unknown"
            },
            "credit_limit": {
                "currency": "AUD",
                "amount": "3000.0"
            },
            "highest_education_attained": self.highest_education_attained,
            "employment_status": self.employment_status,
            "kyc_status": self.kyc_status,
            "last_ok_date": self.last_ok_date
        }

