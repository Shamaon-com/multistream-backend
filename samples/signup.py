import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json
import random
import csv

def create_user(email, password):
    USER_POOL_ID = 'eu-west-1_99F6zJ7ot'
    CLIENT_ID = '5a0g4as2pqrdfg7u3ii5ttt4a4'


    client = boto3.client('cognito-idp')

    try:
        client.sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            Password=password, 
            UserAttributes=[
                {
                    'Name': "email",
                    'Value': email
                }
            ]
        )

    except Exception as e:
        print(e)

    try:
        client.admin_confirm_sign_up(
            UserPoolId=USER_POOL_ID,
            Username=email    
        )
    except Exception as e:
        print(e)


create_user("mariomail1010@gmail.com", "483863")

"""
with open('emailsAndPasswords.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        create_user(row[0], row[1])
        print(row[0], row[1])
"""