import os
import json
import time
import urllib.request
from jose import jwk, jwt
from jose.utils import base64url_decode
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

region = os.environ['REGION']
userpool_id = os.environ['USER_POOL_ID']
app_client_id = os.environ['CLIENT_ID']
keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(
    region, userpool_id)

# instead of re-downloading the public keys every time
# we download them only on cold start
# https://aws.amazon.com/blogs/compute/container-reuse-in-lambda/
with urllib.request.urlopen(keys_url) as f:
    response = f.read()
keys = json.loads(response.decode('utf-8'))['keys']


def lambda_handler(event, context):
    authResponse = {
        'principalId': "Default Response",
        'policyDocument': {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": 'Deny',
                    "Resource": "arn:aws:execute-api:ap-south-1:198309554968:1qmwze1tod/*/*"
                }
            ]
        }
    }

    token = event['queryStringParameters']['authorizer']

    # get the kid from the headers prior to verification
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']
    # search for the kid in the downloaded public keys
    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        logger.info('Public key not found in jwks.json')
        authResponse['policyDocument']['Statement'][0]['Effect'] = 'Deny'
        authResponse['principalId'] = 'Public key not found in jwks.json'
        return authResponse
    # construct the public key
    logger.info('Public key found in jwks.json')
    public_key = jwk.construct(keys[key_index])
    # get the last two sections of the token,
    # message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit('.', 1)
    # decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    # verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        logger.info('Signature verification failed')
        authResponse['policyDocument']['Statement'][0]['Effect'] = 'Deny'
        authResponse['principalId'] = 'Signature verification failed'
        return authResponse
    logger.info('Signature successfully verified')
    # since we passed the verification, we can now safely
    # use the unverified claims
    claims = jwt.get_unverified_claims(token)
    # additionally we can verify the token expiration
    if time.time() > claims['exp']:
        logger.info('Token is expired')
        authResponse['policyDocument']['Statement'][0]['Effect'] = 'Deny'
        authResponse['principalId'] = 'Token is expired'
        return authResponse
    logger.info('Token has not yet been expired')
    # and the Audience  (use claims['client_id'] if verifying an access token)
    if claims['aud'] != app_client_id:
        logger.info('Token was not issued for this audience')
        authResponse['policyDocument']['Statement'][0]['Effect'] = 'Deny'
        authResponse['principalId'] = 'Token was not issued for this audience'
        return authResponse
    # now we can use the claims
    logger.info('Authentication Passed with Claims: %s', claims)
    authResponse['policyDocument']['Statement'][0]['Effect'] = 'Allow'
    authResponse['principalId'] = 'Authentication Passed'
    return authResponse
