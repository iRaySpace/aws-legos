import json
import uuid
import boto3
from botocore.exceptions import ClientError


vehicles_tbl = boto3.resource('dynamodb').Table('vehicles')


def _create(payload):
    payload['id'] = str(uuid.uuid4())
    result = vehicles_tbl.put_item(Item=payload)
    return {
        'statusCode': 201,
        'body': 'created',
    }


def _read(id):
    result = vehicles_tbl.get_item(Key={'id': id})
    if not result.get('Item'):
        return {
            'statusCode': 404,
            'body': 'not found',
        }

    return {
        'statusCode': 200,
        'body': json.dumps(result.get('Item')),
    }


def _update(payload):
    try:
        result = vehicles_tbl.update_item(
            Key={'id': payload['id']},
            UpdateExpression='set #name = :name',
            ExpressionAttributeNames={'#name': 'name'},
            ExpressionAttributeValues={':name': payload['name']},
            ConditionExpression='attribute_exists(id)', # Only if has id
            ReturnValues='ALL_NEW',
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {
                'statusCode': 404,
                'body': 'not found',
            }

        return {
            'statusCode': 500,
            'body': 'internal server error',
        }

    return {
        'statusCode': 200,
        'body': json.dumps(result.get('Attributes')),
    }


def _delete(id):
    vehicles_tbl.delete_item(Key={'id': id})
    return {'statusCode': 204}


def lambda_handler(event, context):
    payload = None
    if event['body']:
        payload = json.loads(event['body'])

    if event['httpMethod'] == 'POST':
        return _create(payload)
    elif event['httpMethod'] == 'GET':
        id = event['pathParameters'].get('id')
        return _read(id)
    elif event['httpMethod'] == 'PUT':
        return _update(payload)
    elif event['httpMethod'] == 'DELETE':
        id = event['pathParameters'].get('id')
        return _delete(id)

    return {
        'statusCode': 500,
        'body': "internal server error",
    }
