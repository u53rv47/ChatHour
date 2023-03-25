import os
from pprint import pprint
import boto3

USERNAME = 'thephilomath'
# PASSWORD = 'Vij88086@ay'
# EMAIL = 'vijaysingh997022@gmail.com'
# NAME = 'Vijay Singh'

CLIENT_ID = '7jeammtmg91nuildl8s3nve8q1'

client = boto3.client('cognito-idp')

CONFIRMATION_CODE = input('Enter code recieved on email: ')

# response = client.sign_up(
#     ClientId=CLIENT_ID,')
response = client.confirm_sign_up(
    ClientId=CLIENT_ID,
    Username=USERNAME,
    ConfirmationCode=CONFIRMATION_CODE,
)

pprint(response)


################ Run to send New code ################

# response = response = client.resend_confirmation_code(
#     ClientId=CLIENT_ID,
#     Username=USERNAME,
# )
