import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('file-metadata')

def lambda_handler(event, context):

    for record in event['Records']:

        body = json.loads(record['body'])
        message = json.loads(body['Message'])

        file_key = message['Records'][0]['s3']['object']['key']

        table.put_item(
            Item={
                'fileName': file_key,
                'status': 'processed',
                'timestamp': datetime.utcnow().isoformat()
            }
        )

        print("Stored metadata for:", file_key)

    return {"statusCode": 200}
