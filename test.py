import boto3
from pprint import pprint

client = boto3.client('cognito-idp')

response = client.describe_user_pool_client(
    UserPoolId='ap-south-1_97yS7nuoM',
    ClientId='7jeammtmg91nuildl8s3nve8q1'
)
pprint(response)
