import boto3
import os
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    connections_table = dynamodb.Table(os.environ['CONNECTIONS_TABLE'])
    response = connections_table.delete_item(
        Key={
            'connectionId': event['requestContext']['connectionId']})

    logger.info("Response: %s", response)

    response = {
        "statusCode": 200,
        'body':  "Disconnected Successfully"
    }
    logger.info("onDisconnect response: %s", response)
    return response
