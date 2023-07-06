data "aws_iam_policy_document" "iam_policy_document" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["arn:aws:logs:*:*:*"]
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name = "${var.region}-${var.application}-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "iam_policy_for_lambda" {
  name = "${var.region}-${var.application}-policy"
  role = aws_iam_role.iam_for_lambda.id

  policy = data.aws_iam_policy_document.iam_policy_document.json
}

resource "aws_lambda_function" "lambda_function" {
  filename      = "../function.zip"
  function_name = "${var.application}-lambda"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda_function.lambda_handler"

  layers = [
    aws_lambda_layer_version.selenium.arn,
    "arn:aws:lambda:us-east-1:599129187124:layer:chromedriver:1"
  ]

  source_code_hash = filebase64sha256("../function.zip")

  runtime = "python3.9"

}


resource "aws_lambda_layer_version" "selenium" {
  filename            = "../python.zip"
  layer_name          = "selenium"
  source_code_hash    = filebase64sha256("../python.zip")
  compatible_runtimes = ["python3.9"]
}

resource "aws_lambda_layer_version" "chromedriver" {
  s3_bucket           = aws_s3_bucket.lambda_packages.id
  s3_key              = "chromedriver.zip"
  layer_name          = "chromedriver"
  source_code_hash    = filebase64sha256("../chromedriver.zip")
  compatible_runtimes = ["python3.9"]
}


resource "aws_s3_bucket" "lambda_packages" {
  bucket = "de-aws-lambda-packages"
}

resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_function.function_name
  principal     = "apigateway.amazonaws.com"
}
