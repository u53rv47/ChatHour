import boto3

from pprint import pprint

client = boto3.client('cognito-idp')

response = client.admin_initiate_auth(
    ClientId='7jeammtmg91nuildl8s3nve8q1',
    UserPoolId='ap-south-1_97yS7nuoM',
    AuthFlow='ADMIN_USER_PASSWORD_AUTH',
    AuthParameters={
        'USERNAME': 'u53rv47',
        'PASSWORD': 'Vij88086@ay'
    }

)
with open('auth_response.txt', 'w') as outfile:
    outfile.write(response['AuthenticationResult']['IdToken'])

pprint(response)
