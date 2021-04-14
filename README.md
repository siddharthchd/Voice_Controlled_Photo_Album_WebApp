# **Voice Controlled Photo Album**
 
The photo album is a web application that can be searched using natural language through both text and voice. This web application was developed as part of the course project assignment for the course - Cloud Computing (CS-GY:9223, NYU Tandon) 


# Table of contents
* [Description](#description)
* [Technologies](#technologies)
* [Workflow](#workflow)


## Description

The photo album is a scalable web application designed and deployed using AWS services like S3, Lex and ElasticSearch. CI/CD DevOps pipeline is used to automate the build, test and deploy phases. The application allows users to make search requests, display the search results resulting from the query as well as upload new photos. The user is also given a choice to use either voice or text to perform the search queries.


![Chatbot Demo](https://github.com/siddharthchd/Voice_Controlled_Photo_Album_WebApp/blob/main/FrontEnd/FrontEndUI.png)
<br>

## Technologies

* Python
* Javascript
* HTML
* CSS
* AWS - Simple Storage Service (S3)
* AWS - API Gateway
* AWS - Lambda
* AWS - Lex
* AWS - ElasticSearch
* AWS - Rekognition
* AWS - Transcribe
* AWS - Cloudwatch
* AWS - CloudFront
* AWS - CodePipeline
* AWS - Cloudformation
* AWS - CodeBuild


## Workflow

* The frontend for the application is hosted in an S3 bucket as a static website.
* Using the AWS ElasticSearch service a domain is set up so that when a photo gets uploaded to the bucket, lambda funciton is triggered to index it.
* Labels are detected in the image using Rekognition. A JSON object with a reference to each object in the S3 is stored in an ElasticSearch index, for every label detected by the Rekognition service.
* A lambda function called 'search-photos' is used as a code hook for the Lex service in order to detect the search keywords.
* Amazon Lex bot is created to handle search queries for which an intent called 'SearchIntent' is created and training utterances are added to the intent.

The following is the architecture for this project, to understand the workflow:-
![Chatbot Architecture](https://github.com/siddharthchd/Voice_Controlled_Photo_Album_WebApp/blob/main/Architecture/diagram.png)
