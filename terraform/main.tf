# Lambda 
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

  depends_on = [
    null_resource.ecr_image
  ]

  function_name = "${var.application}-lambda"
  role          = aws_iam_role.iam_for_lambda.arn
  image_uri     = "${aws_ecr_repository.repo.repository_url}@${data.aws_ecr_image.lambda_image.id}"
  package_type  = "Image"
  timeout       = 300

}


## ECR

resource "aws_ecr_repository" "repo" {
  name                 = "${var.application}-ecr"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}

resource "null_resource" "ecr_image" {
  triggers = {
    python_file = md5(file("${path.module}/${local.app_dir}/main.py"))
    docker_file = md5(file("${path.module}/${local.app_dir}/Dockerfile"))
  }

  provisioner "local-exec" {
    command = <<EOF
      aws ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin ${local.account_id}.dkr.ecr.${var.region}.amazonaws.com
      cd ${path.module}/${local.app_dir}
      docker build -t ${aws_ecr_repository.repo.repository_url}:latest .
      docker push ${aws_ecr_repository.repo.repository_url}:latest
    EOF
  }
}

data "aws_ecr_image" "lambda_image" {
  repository_name = "${var.application}-ecr"
  image_tag       = "latest"
}
