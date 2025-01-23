import os
import json
import urllib3


http = urllib3.PoolManager()


def lambda_handler(event, context):
    messages_length = len(event['Records'])
    for record in event['Records']:
        http.request(
            'POST',
            os.environ.get('DISCORD_WEBHOOK_URL'),
            body=json.dumps({'content': f'Message from SQS: {record.get("body")}'}),
            headers={'Content-Type': 'application/json'},
            retries=False,
        )
    return {
        'statusCode': 200,
        'body': json.dumps(f'Processed {messages_length} messages!')
    }
