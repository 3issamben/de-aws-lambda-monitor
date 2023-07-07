# DE Lambda monitor

This project deploys an AWS Lambda function with Terraform. The Lambda function uses a Python script with Selenium to monitor API endpoints.

## Repository Structure

```bash
├── README.md
├── app
│   ├── Dockerfile 
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

## Deployment
Run the following commands to deploy lambda function including building new docker image


```
terraform init
terraform plan
terraform apply
```
## Note

