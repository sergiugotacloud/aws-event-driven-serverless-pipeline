
Event-driven serverless architecture on AWS using S3, SNS, SQS, Lambda and DynamoDB.

This project demonstrates a small event driven architecture built on AWS.

The goal was to build a system where uploading a file automatically triggers multiple independent processing steps without tightly coupling the services together.

Instead of sending the upload directly to a single processor, the system publishes an event and allows different consumers to react to it independently. This makes the architecture easier to scale and extend later.

Architecture

![Architecture Diagram](architecture/architecture-diagram.png)

How the system works

1. A client uploads a file to Amazon S3  
2. S3 generates an ObjectCreated event  
3. The event is sent to an SNS topic  
4. SNS distributes the message to multiple SQS queues  
5. Each queue triggers a different Lambda function  
6. The metadata Lambda stores file information in DynamoDB  
7. Lambda executions are recorded in CloudWatch Logs  

Architecture decisions

Amazon S3

S3 is used as the entry point of the system.

Reasons

1. Durable object storage  
2. Built in event notification system  
3. Direct integration with other AWS services  

Amazon SNS

SNS is responsible for distributing the event.

Reasons

1. Enables fan out messaging  
2. Allows multiple consumers to react to the same event  
3. Keeps producers and consumers independent  

Amazon SQS

SQS queues sit between the event layer and the compute layer.

Two queues are used

Image processing queue  
Metadata processing queue  

Reasons

1. Decouples services  
2. Buffers traffic spikes  
3. Provides reliable message delivery  
4. Enables asynchronous processing  

AWS Lambda

Lambda functions process the messages coming from the queues.

Two functions exist in this project

image processor  
metadata processor  

Reasons

1. Serverless compute  
2. Automatic scaling  
3. No infrastructure management  
4. Native integration with SQS  

Amazon DynamoDB

DynamoDB stores metadata about uploaded files.

Reasons

1. Serverless database  
2. Low latency reads and writes  
3. Automatically scales with workload  

Amazon CloudWatch Logs

CloudWatch is used to observe Lambda execution.

Reasons

1. Centralized logging  
2. Useful for debugging serverless workloads  
3. Helps understand the event flow through the system  

Project structure

aws-event-driven-serverless-pipeline  
│  
├── architecture  
│   └── architecture-diagram.png  
│  
├── lambda  
│   ├── image-processor.py  
│   └── metadata-processor.py  
│  
├── screenshots  
│   ├── 01_s3_bucket.png  
│   ├── 02_s3_event_notification.png  
│   ├── 03_sns_topic.png  
│   ├── 04_sqs_queues.png  
│   ├── 05_sns_subscriptions.png  
│   ├── 06_lambda_functions.png  
│   ├── 07_lambda_triggers.png  
│   ├── 08_dynamodb_table.png  
│   ├── 09_cloudwatch_logs.png  
│   └── 10_dynamodb_result.png  
│  
├── README.md  
├── LICENSE  
└── .gitignore  

Screenshots

S3 bucket

![S3 Bucket](screenshots/01_s3_bucket.png)

SNS topic

![SNS Topic](screenshots/03_sns_topic.png)

SQS queues

![SQS Queues](screenshots/04_sqs_queues.png)

Lambda functions

![Lambda Functions](screenshots/06_lambda_functions.png)

DynamoDB result

![DynamoDB Result](screenshots/10_dynamodb_result.png)

Things I learned while building this

Building the architecture in the AWS console highlighted how important service permissions are. S3 cannot publish to SNS without the correct topic policy, and Lambda cannot read from SQS without the proper IAM role permissions.

Another important lesson was how useful SQS is for decoupling systems. Even though both Lambda functions react to the same event, they operate independently and can scale separately.

Working with the event payload also helped clarify how AWS services pass structured events through multiple layers. The Lambda functions need to unpack the SQS message, then the SNS message, and finally the original S3 event to extract the file information.

Finally, seeing the entire flow from S3 upload to DynamoDB record reinforced how powerful serverless architectures can be when services are connected through events rather than direct calls.
