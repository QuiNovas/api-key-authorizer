import boto3
import hashlib
import logging.config
import os


def handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    api_key = event['authorizationToken']
    # If this starts with 'Bearer ' then we are receiving this
    # from the Authorization header and need to sub-string
    if api_key.startswith('Bearer '):
        api_key = api_key[7:]
    logger.info('Client Token: {}'.format(api_key))
    logger.info('Method ARN: {}'.format(event['methodArn']))

    if len(api_key) == 0:
        logger.warn('Incomplete authentication - no api key present')
        raise Exception('Unauthorized')

    dynamodb = boto3.resource('dynamodb')

    api_keys_table = dynamodb.Table(os.environ['API_KEYS_TABLE_NAME'])

    api_key_response = api_keys_table.get_item(
        Key={
            'Apikey': hashlib.sha256(api_key).hexdigest()
        }
    )

    if 'Item' not in api_key_response:
        logger.info('API Key {} not in table {}'.format(api_key, os.environ['API_KEYS_TABLE_NAME']))
        raise Exception('Unauthorized')

    groups_table = dynamodb.Table(os.environ['GROUPS_TABLE_NAME'])

    policy_response = groups_table.get_item(
        Key={
            'GroupId': api_key_response['Item']['GroupId']
        }
    )

    if 'Item' not in policy_response:
        logger.error('GroupId {} not in table {}'.format(api_key_response['Item']['GroupId'], os.environ['GROUPS_TABLE_NAME']))
        raise Exception('Unauthorized')

    logger.info('Setting policy {} for api key {}'.format(policy_response['Item']['Policy'], api_key))

    return {
        'principalId': api_key,
        'policyDocument': policy_response['Item']['Policy'],
        'usageIdentifierKey': api_key
    }
