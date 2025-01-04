# Setup Guide

This guide provides step-by-step instructions for setting up the AWS resources required for the Text-to-Speech Converter project.

## Prerequisites

Before starting, ensure you have the following:
- An AWS account with permissions to manage DynamoDB, S3, Lambda, SNS, and API Gateway.
- AWS CLI installed and configured with access keys.
- A text editor or IDE for writing Lambda functions.
- Node.js installed (optional, for hosting the static website).

---

## Steps to Set Up AWS Resources

### 1. Create a DynamoDB Table
1. Sign in to the [AWS Management Console](https://aws.amazon.com/console/).
2. Navigate to **DynamoDB** > **Tables**.
3. Click on **Create Table**.
4. Configure the table:
   - **Table Name:** `PostsTable`
   - **Partition Key:** `PostId` (String)
5. Leave all other settings as default and click **Create Table**.

### 2. Create an Amazon S3 Bucket
1. Navigate to **S3** in the AWS Console.
2. Click **Create Bucket**.
3. Configure the bucket:
   - **Bucket Name:** `text-to-speech-audio` (choose a globally unique name).
   - **Region:** Same as other resources.
4. Enable **public access** for the bucket (temporary for testing purposes).
5. Click **Create Bucket**.

### 3. Create an SNS Topic
1. Navigate to **SNS** in the AWS Console.
2. Click **Topics** > **Create Topic**.
3. Configure the topic:
   - **Type:** Standard
   - **Name:** `NewPostTopic`
4. Click **Create Topic**.
5. Note down the **Topic ARN** for later use.

### 4. Create Lambda Functions

#### a. New Post Lambda Function
1. Navigate to **Lambda** > **Create Function**.
2. Select **Author from scratch**.
3. Configure the function:
   - **Function Name:** `NewPostFunction`
   - **Runtime:** Python 3.x
4. Click **Create Function**.
5. Add the code to handle API Gateway requests and interact with DynamoDB (to be added in the `scripts` folder).

#### b. Convert to Audio Lambda Function
Repeat the steps above but name the function `ConvertToAudioFunction`. This function will:
- Subscribe to the SNS topic.
- Use Amazon Polly to convert text to audio.
- Save the audio to the S3 bucket.

#### c. Get Post Lambda Function
Repeat the steps above but name the function `GetPostFunction`. This function retrieves post details from DynamoDB.

### 5. Configure API Gateway
1. Navigate to **API Gateway** > **Create API**.
2. Select **REST API** > **Build**.
3. Create two endpoints:
   - **POST** `/newpost` (linked to `NewPostFunction`)
   - **GET** `/getpost` (linked to `GetPostFunction`)
4. Deploy the API to a stage (e.g., `prod`).

### 6. Deploy the Static Website
1. Upload your static website files to the S3 bucket.
2. Enable **Static Website Hosting** under the bucket properties.
3. Note down the endpoint URL for accessing the website.

---

## Verification
- Use the static website to send and retrieve posts.
- Check DynamoDB for stored post data.
- Verify audio files in the S3 bucket.

---

You are now ready to use the Text-to-Speech Converter application!

