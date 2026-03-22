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
  description = "AWS region for this dev/test database"
  type        = string
  default     = "ap-southeast-2"
}

variable "db_subnet_ids" {
  description = "Subnet IDs where the RDS instance will run (normally private subnets inside the dev/test VPC)."
  type        = list(string)
}

variable "db_security_group_id" {
  description = "Security group ID that controls network access to the RDS instance."
  type        = string
}

variable "db_name" {
  description = "Initial database name for wordloom-v3 cloud-dev."
  type        = string
  default     = "wlv3_cloud_dev"
}

variable "db_username" {
  description = "Master username for the dev/test Postgres instance."
  type        = string
}

variable "db_password" {
  description = "Master password for the dev/test Postgres instance. Do not commit actual values; pass via tfvars or environment variables."
  type        = string
  sensitive   = true
}

variable "db_instance_class" {
  description = "RDS instance class for dev/test."
  type        = string
  default     = "db.t4g.micro"
}

resource "aws_db_subnet_group" "devtest" {
  name       = "wlv3-cloud-dev-db-subnets"
  subnet_ids = var.db_subnet_ids

  tags = {
    Name        = "wlv3-cloud-dev-db-subnets"
    Project     = "wordloom-v3"
    Environment = "cloud-dev"
  }
}

resource "aws_db_instance" "devtest" {
  identifier              = "wlv3-cloud-dev-postgres"
  engine                  = "postgres"
  engine_version          = "16.3"
  instance_class          = var.db_instance_class
  allocated_storage       = 20
  db_name                 = var.db_name
  username                = var.db_username
  password                = var.db_password
  db_subnet_group_name    = aws_db_subnet_group.devtest.name
  vpc_security_group_ids  = [var.db_security_group_id]
  publicly_accessible     = false
  skip_final_snapshot     = true
  deletion_protection     = false
  backup_retention_period = 0

  tags = {
    Name        = "wlv3-cloud-dev-postgres"
    Project     = "wordloom-v3"
    Environment = "cloud-dev"
  }
}

output "db_endpoint" {
  description = "Connection endpoint for the dev/test Postgres instance."
  value       = aws_db_instance.devtest.endpoint
}

output "db_port" {
  description = "Port exposed by the dev/test Postgres instance."
  value       = aws_db_instance.devtest.port
}

output "db_identifier" {
  description = "RDS instance identifier."
  value       = aws_db_instance.devtest.id
}
