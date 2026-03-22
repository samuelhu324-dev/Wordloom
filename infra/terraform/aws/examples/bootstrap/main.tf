terraform {
  required_version = ">= 1.4.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region for this example"
  type        = string
  default     = "ap-southeast-2"
}

variable "bucket_name" {
  description = "Name of the S3 bucket to create (must be globally unique if you ever apply)."
  type        = string
  default     = "samuelhu-wlv3-bootstrap-example-01"
}

resource "aws_s3_bucket" "bootstrap" {
  bucket = var.bucket_name

  tags = {
    Project     = "wordloom-v3"
    Environment = "cloud-dev"
    Purpose     = "terraform-bootstrap-example"
  }
}
