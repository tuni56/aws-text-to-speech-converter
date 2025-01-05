# Setup Guide

This guide provides step-by-step instructions for setting up the AWS resources required for the Text-to-Speech Converter project using AWS CLI.

## Prerequisites

Before starting, ensure you have the following:

- An AWS account with permissions to manage DynamoDB, S3, Lambda, SNS, and API Gateway.
- AWS CLI installed and configured with access keys.
- A text editor or IDE for writing Lambda functions.
- Node.js installed (optional, for hosting the static website).

---

## Steps to Set Up AWS Resources

### 1. Create a DynamoDB Table

1. Open your terminal and use the following AWS CLI command:
   ```bash
   aws dynamodb create-table \
       --table-name PostsTable \
       --attribute-definitions AttributeName=PostId,AttributeType=S \
       --key-schema AttributeName=PostId,KeyType=HASH \
       --billing-mode PAY_PER_REQUEST  
   ```
2. Verify the table creation:
   ```bash
   aws dynamodb list-tables
   ```

### 2. Create an Amazon S3 Bucket

1. Run the following command to create a bucket:
   ```bash
   aws s3 mb s3://text-to-speech-audio
   ```
2. Enable public access (temporary for testing purposes):
   ```bash
   aws s3api put-bucket-acl --bucket text-to-speech-audio --acl public-read
   ```
3. Verify the bucket creation:
   ```bash
   aws s3 ls
   ```

### 3. Create an SNS Topic

1. Create a new topic:
   ```bash
   aws sns create-topic --name NewPostTopic
   ```
2. Note the ARN returned in the output: `arn:aws:sns:us-east-1:452298468714:NewPostTopic`
3. Verify the topic creation:
   ```bash
   aws sns list-topics
   ```

### 4. Create Lambda Functions

#### a. New Post Lambda Function

1. Write your function code locally (e.g., `new_post_function.py`). Ensure your code references the SNS topic ARN `arn:aws:sns:us-east-1:452298468714:NewPostTopic`. Example Python code snippet:
   ```python
   import boto3
   import json

   sns_client = boto3.client('sns')
   sns_topic_arn = 'arn:aws:sns:us-east-1:452298468714:NewPostTopic'

   def lambda_handler(event, context):
       message = json.dumps(event['body'])
       sns_client.publish(TopicArn=sns_topic_arn, Message=message)
       return {
           'statusCode': 200,
           'body': 'Post received and SNS message sent.'
       }
   ```
2. Zip the function code:
   ```bash
   zip NewPostFunction.zip new_post_function.py
   ```
3. Create the Lambda function:
   ```bash
   aws lambda create-function \
       --function-name NewPostFunction \
       --runtime python3.x \
       --role <IAM-ROLE-ARN> \
       --handler new_post_function.lambda_handler \
       --zip-file fileb://NewPostFunction.zip
   ```
4. Verify the function creation:
   ```bash
   aws lambda list-functions
   ```

#### b. Convert to Audio Lambda Function

Repeat the steps above, replacing `NewPostFunction` with `ConvertToAudioFunction` and using the appropriate code file.

#### c. Get Post Lambda Function

Repeat the steps above, replacing `NewPostFunction` with `GetPostFunction` and using the appropriate code file.

### 5. Configure API Gateway

1. Create a new REST API:
   ```bash
   aws apigateway create-rest-api --name TextToSpeechAPI
   ```
2. Note the API ID returned in the output.
3. Create a resource for `/newpost`:
   ```bash
   aws apigateway create-resource --rest-api-id <API-ID> --parent-id <PARENT-ID> --path-part newpost
   ```
4. Link the resource to the `NewPostFunction` Lambda:
   ```bash
   aws apigateway put-method --rest-api-id <API-ID> --resource-id <RESOURCE-ID> --http-method POST --authorization-type NONE
   aws apigateway put-integration --rest-api-id <API-ID> --resource-id <RESOURCE-ID> --http-method POST --type AWS_PROXY --integration-http-method POST --uri arn:aws:apigateway:<REGION>:lambda:path/2015-03-31/functions/arn:aws:lambda:<REGION>:<ACCOUNT-ID>:function:NewPostFunction/invocations
   ```
5. Repeat the above steps for `/getpost`.
6. Deploy the API:
   ```bash
   aws apigateway create-deployment --rest-api-id <API-ID> --stage-name prod
   ```

### 6. Deploy the Static Website

1. Upload your static website files to the S3 bucket:
   ```bash
   aws s3 cp <LOCAL-PATH> s3://text-to-speech-audio/ --recursive
   ```
2. Enable static website hosting:
   ```bash
   aws s3 website s3://text-to-speech-audio/ --index-document index.html
   ```
3. Note the website endpoint URL.

---

## Verification

- Use the static website to send and retrieve posts.
- Check DynamoDB for stored post data:
  ```bash
  aws dynamodb scan --table-name PostsTable
  ```
- Verify audio files in the S3 bucket:
  ```bash
  aws s3 ls s3://text-to-speech-audio/
  ```

---

You are now ready to use the Text-to-Speech Converter application!

