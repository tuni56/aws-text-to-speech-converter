# AWS Text-to-Speech Converter

This project demonstrates how to build a serverless text-to-speech converter using AWS services like DynamoDB, Lambda, S3, SNS, Polly, and API Gateway.

## Features
- Store and manage posts using DynamoDB.
- Convert text posts into audio files (MP3) with Amazon Polly.
- Serve the audio files via S3 and provide RESTful API access.
- Static web interface for easy interaction.

## Architecture Overview
The application is designed using a serverless architecture, ensuring scalability, cost-effectiveness, and ease of maintenance.

## Getting Started
Follow these steps to deploy and run the project.

### Prerequisites
- An AWS account with sufficient permissions.
- AWS CLI installed and configured.
- Node.js installed (for setting up the static website).
- Python 3.x for Lambda functions.

### Steps to Deploy
1. **Create AWS Resources:**
   - DynamoDB table
   - S3 bucket
   - SNS topic
2. **Deploy Lambda Functions:**
   - `new_post_lambda`
   - `convert_to_audio_lambda`
   - `get_post_lambda`
3. **Expose APIs using API Gateway.**
4. **Host the static website on S3.**

## Usage
- Access the web interface hosted on Amazon S3.
- Use the "Add Post" form to submit text for conversion.
- Retrieve posts via the "Get Post" section.

## Contributing
Contributions are welcome! Please submit a pull request or raise an issue for suggestions.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

