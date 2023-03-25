import os
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    connections_table = dynamodb.Table(os.environ['CONNECTIONS_TABLE'])
    response = connections_table.put_item(
        Item={
            'connectionId': event['requestContext']['connectionId']})

    logger.info("Response: %s", response)

    response = {
        "statusCode": 200,
        'body':  "Connected Successfully"
    }
    logger.info("onConnect response: %s", response)
    return response
