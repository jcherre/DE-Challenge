# Globant's Data Engineer CHallenge
## Introduction

This repo contains my proposed approach for the data engineer challenge. All the info and files from the challenge are inside the docs folder. Other branches were made for proof of concepts and testing, the whole history is being shared for you to see the process of development. There is also a results folder for some output CSV files and captures :thumbsup:

## Solution

Considering a stack using **Flask** framework for the backend API, **PostgreSQL** as DB with **SQLAlchemy** to handle the transactions, and **pandas** for processing and cleaning, this is the image of the proposed architecture for a cloud implementation:

![Architecture](https://github.com/jcherre/DE-Challenge/tree/main/proposed_architecture.png)

The solution proposes the following services:
* **Cloud Run** to execute the containerized code for the API in **Google Artifact Registry**
* **Cloud SQL for PostgreSQL** as the database
* **Cloud Build** with custom triggers for CI/CD through **Github**
* All services are inside a **VPC** to be accessed only inside the internal network

This solution allows to tackle the cases presented in the problem; nonetheless, for scalability I recommend to use **Cloud Storage** and **Dataflow** for a more robust ingestion approach with CSV files in the size of GB.

For a production environment, the Cloud Run service is launched through gunicorn and the environment variables are passed in the Cloud Build trigger. For a better approach, we could use **Cloud Secrets Manager** to replace the variables with secrets stored in a secure space.

---
## Setup

For a local setup, the line app.run should be uncommented and the env variables should be set appropiately:
1. **API_TOKEN**: Token for authenticating the request
2. **GOOGLE_APPLICATION_CREDENTIALS**: route with the appropiate JSON keys from the service account to use the services
3. **PROJECT_ID**: ID of project in GCP
4. **REGION**: Location of the Cloud SQL instance
5. **INSTANCE**: Name of the Cloud SQL instance
6. **DB_USER**: User of the Cloud SQL instance
7. **DB_PASS**: Password of the Cloud SQL instance
8. **DB_NAME**: Name of the DB in the Cloud SQL instance
9. **PUBLIC_IP**: Flag for using public IP to connect to the Cloud SQL instance, don't pass it if deploying with VPC **[Unless you configure Cloud Proxy, you should enable public IP access in your instance and allow your local IP for access]**

The tests in test_api.py can be used to test the API functionality or you could check with some querying in your Cloud SQL instance. In case you need to setup the DB tables as well, the script is located in the DDL folder.

For a cloud implementation you should create the following services:
1. VPC and VPC connector
2. Cloud SQL for PostgreSQL instance, configure only private IPs for access through VPC in a secure network
3. Configure the necessary service account with permission for Cloud SQL Client and Cloud Run Service Agent
4. Configure Cloud Build to connect to the repo for CI/CD and set up triggers with enviroment variables

Once everything is configured, the *cloudbuild.yaml* file gets in charge of the automated testing and deployment using pytest library. If all the necessary test cases are passed, the trigger will update the Cloud Run with the image changes. Otherwise it will fail and the output will be logged to Cloud Logging.

## Recommendations and future work

The libraries used in the server code (pandas, SQLAlchemy) are good for batch processing but lack some capability for Big Data handling. In a bigger scenario, it is recommended to leverage other tools like Beam or PySaprk for data processing. Also, we could use Compute Engine capabilities in case the app needs more complex components and to handle traffic and files bigger than 32GB which is the memory limit for this service. Finally, for automation of the deployment, we could use Hashicorp Terraform and automate the whole setup in cloud with only a JSON configuration file.

