terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }

  # Remote state backend — required so Terraform remembers what it already
  # created between GitHub Actions runs. Replace the bucket name with your
  # own (created manually, one-time, in the AWS Console).
  backend "s3" {
    bucket         = "abhishek-kumar-tf-state-2026"
    key            = "bedrock-chatbot/terraform.tfstate"
    region         = "eu-north-1"
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region
}
