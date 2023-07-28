# DE Lambda monitor

This project deploys an AWS Lambda function with Terraform. The Lambda function uses a Python script with Selenium to monitor API endpoints.

## Repository Structure

```bash
├── README.md
├── app
│   ├── Dockerfile
    ├── tests/ # contains unit test
│   ├── main.py # main lambda code
│   └── requirements.txt # python dependencies
└── terraform
    ├── locals.tf
    ├── main.tf
    ├── outputs.tf
    ├── provider.tf
    ├── terraform.tfvars
    └── variables.tf
```    

## Infrastructure Deployment
Run the following commands to deploy lambda function including building new docker image


```
terraform init
terraform plan
terraform apply
```
## Local Development

You can run the docker container using the following commands
```
 docker build -t de-aws-lambda-monitor .
 docker run -p 9000:8080 de-aws-lambda-monitor:latest
```

Send a request to the lambda function using the curl command
```
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```

**Note**: You can supply the `puller_id` in the body request to process task from specific puller_id otherwise the default value of puller_id is `11`

## Tests

The project contains unit tests.

In order to run the tests run the following command

1. Install test modules
```
pip install -r tests/requirements.txt
```

2. Run unit test
```
python -m pytest tests/
```