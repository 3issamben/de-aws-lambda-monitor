provider "aws" {
  region = var.region
  default_tags {
    tags = {
      Environment = "test"
      Owner       = "issam"
      Application = "de-aws-monitor"
    }
  }
}
