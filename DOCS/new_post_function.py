import json
import boto3
import uuid
from botocore.exceptions import ClientError

# Inicializar clientes de AWS
dynamodb = boto3.client('dynamodb')
sns = boto3.client('sns')

# Nombre de la tabla de DynamoDB y ARN del tema de SNS
DYNAMODB_TABLE = 'PostsTable'
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:452298468714:NewPostTopic'

def lambda_handler(event, context):
    try:
        # Parsear la entrada
        body = json.loads(event['body'])
        post_id = str(uuid.uuid4())
        text = body['text']
        language = body['language']
        
        # Insertar en DynamoDB
        dynamodb.put_item(
            TableName=DYNAMODB_TABLE,
            Item={
                'PostId': {'S': post_id},
                'Text': {'S': text},
                'Language': {'S': language},
                'Status': {'S': 'Pending'}
            }
        )
        
        # Publicar en el tema de SNS
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=json.dumps({'PostId': post_id}),
            Subject='New Post Created'
        )
        
        # Responder al cliente
        response = {
            'statusCode': 200,
            'body': json.dumps({'message': 'Post created successfully', 'PostId': post_id})
        }
    except ClientError as e:
        response = {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    
    return response
