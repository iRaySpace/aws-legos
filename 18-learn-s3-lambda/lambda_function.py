import os
import json
import urllib3


http = urllib3.PoolManager()


def lambda_handler(event, context):
    s3_event = event.get('Records')[0].get('s3')
    r = http.request(
        'POST',
        os.environ.get('DISCORD_WEBHOOK_URL'),
        body=json.dumps({"content": f"File {s3_event.get('object').get('key')} is uploaded to {s3_event.get('bucket').get('name')}!"}),
        headers={'Content-Type': 'application/json'},
        retries=False,
    )
    return {
        'status': r.status,
        'body': json.dumps('Discord is notified!'),
    }
