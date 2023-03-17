import os
from pprint import pprint
import boto3

USERNAME = 'u53rv47'
PASSWORD = 'Vij88086@ay'
EMAIL = 'vijaysingh997022@gmail.com'
NAME = 'Vijay Singh'

CLIENT_ID = '7jeammtmg91nuildl8s3nve8q1'


client = boto3.client('cognito-idp')
response = client.sign_up(
    ClientId=CLIENT_ID,
    Username=USERNAME,
    Password=PASSWORD,
    UserAttributes=[
        {
            'Name': 'email',
            'Value': EMAIL
        },
        {
            'Name': 'name',
            'Value': NAME
        },

    ],
    ValidationData=[
        {
            'Name': 'email',
            'Value': NAME
        },
    ]
)

pprint(response)
