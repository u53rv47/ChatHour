import os
import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb_client = boto3.client('dynamodb')


def lambda_handler(event, context):
    message = json.loads(event['body']['message'])

    paginator = dynamodb_client.get_paginator('scan')
    connectionIds = []
    for page in paginator.paginate(TableName=os.environ['CONNECTIONS_TABLE']):
        connectionIds.extend(page['Items'])

    apigatewaymanagementapi = boto3.client(
        'apigatewaymanagementapi',
        endpoint_url="https://" +
        event["requestContext"]["domainName"] + '/' +
        event["requestContext"]["stage"]
    )

    for connectionId in connectionIds:
        apigatewaymanagementapi.post_to_connection(
            Data=message,
            ConnectionId=connectionId['connectionId']['S"']
        )

    response = {
        "statusCode": 200,
        'body':  "message sent Successfully"
    }
    logger.info("sendMessage response: %s", response)
    return response
