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
  description = "AWS region for this dev/test network"
  type        = string
  default     = "ap-southeast-2"
}

variable "vpc_cidr" {
  description = "CIDR block for the dev/test VPC"
  type        = string
  default     = "10.42.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for the public subnet in ap-southeast-2a"
  type        = string
  default     = "10.42.0.0/24"
}

resource "aws_vpc" "cloud_dev" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name        = "wlv3-cloud-dev-vpc"
    Project     = "wordloom-v3"
    Environment = "cloud-dev"
  }
}

resource "aws_subnet" "public_a" {
  vpc_id                  = aws_vpc.cloud_dev.id
  cidr_block              = var.public_subnet_cidr
  availability_zone       = "ap-southeast-2a"
  map_public_ip_on_launch = true

  tags = {
    Name        = "wlv3-cloud-dev-public-a"
    Project     = "wordloom-v3"
    Environment = "cloud-dev"
    Tier        = "public"
  }
}

resource "aws_security_group" "cloud_dev_basic" {
  name        = "wlv3-cloud-dev-sg-basic"
  description = "Basic security group for wordloom-v3 dev/test"
  vpc_id      = aws_vpc.cloud_dev.id

  # 暂时允许所有出站流量，入站规则后续在 devtest-db 等模块中细化
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "wlv3-cloud-dev-sg-basic"
    Project     = "wordloom-v3"
    Environment = "cloud-dev"
  }
}

output "vpc_id" {
  description = "ID of the dev/test VPC"
  value       = aws_vpc.cloud_dev.id
}

output "public_subnet_id" {
  description = "ID of the public subnet in ap-southeast-2a"
  value       = aws_subnet.public_a.id
}

output "basic_sg_id" {
  description = "ID of the basic dev/test security group"
  value       = aws_security_group.cloud_dev_basic.id
}
