
try:
    from flask import Flask
    from flask_restful import Resource, Api, reqparse
    import sys
    import os
    import json
    import requests
    from flask import request
except Exception as e:
    print("Some Modules are Missing  ")


app = Flask(__name__)
api = Api(app)


global SEND_GRID_TOKEN
global API_END_POINT_SENDGRID

SEND_GRID_TOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
API_END_POINT_SENDGRID = "https://api.sendgrid.com/v3/validations/email"


class EmailVerification(Resource):

    def __init__(self):
        self.emails = parser.parse_args().get('emails', None)

    def get(self):
        try:
            return EmailProcessor.process(emails=self.emails)
        except Exception as e:
            return {"Message":"Something went wrong "}



class EmailProcessor(object):

    @staticmethod
    def process(emails=None):
        try:
            email_tem = []
            email_resp = []

            if emails is not None:
                if len(emails) >= 1:
                    for email in emails.split(","):
                        helper = Emails()
                        response = helper.get(email=email)
                        email_tem.append(email)
                        email_resp.append(response)
                    data = dict(zip(email_tem, email_resp))
                    return data
            if emails is None:
                return {"Message": "Emails are None"}
        except Exception as e:
            return {"Message ": "Something went wrong"},500


class Emails(object):

    __slots__ = ["_headers", "_url"]

    def __init__(self):
        self._headers = {
            'Authorization': SEND_GRID_TOKEN,
            'Content-Type': 'application/json'}
        self._url = API_END_POINT_SENDGRID

    def get(self, email=None):
        try:
            Payload = {
                "email":email,
                'source':"signup"}

            Payload = json.dumps(Payload)
            r = requests.post(url=self._url, headers=self._headers, data=Payload)
            return r.json()
            #return {"Message": "Ok Emails "}
        except Exception as e:
            print(e)
            return {"Message":"Failed to Process email"}, 500


parser = reqparse.RequestParser()

parser.add_argument("emails", type=str, required=True, help="emails seperated by comma  [String]")
api.add_resource(EmailVerification, '/')


if __name__ == '__main__':
    app.run(debug=True)
