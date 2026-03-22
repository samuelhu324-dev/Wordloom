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

locals {
  effective_db_security_group_id = coalesce(var.db_security_group_id, var.db_sg_id)
}

variable "aws_region" {
  description = "AWS region for this dev/test database"
  type        = string
  default     = "ap-southeast-2"
}

variable "db_subnet_ids" {
  description = "Subnet IDs where the RDS instance will run (normally private subnets inside the dev/test VPC)."
  type        = list(string)

  validation {
    condition     = length(var.db_subnet_ids) >= 2
    error_message = "db_subnet_ids must include at least two subnet IDs, ideally across two AZs, for the RDS subnet group."
  }
}

variable "db_security_group_id" {
  description = "Security group ID that controls network access to the RDS instance."
  type        = string
  default     = null
  nullable    = true
}

variable "db_sg_id" {
  description = "Legacy alias for db_security_group_id. Prefer db_security_group_id going forward."
  type        = string
  default     = null
  nullable    = true
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

variable "db_engine_version" {
  description = "Optional Postgres engine version. Leave null to let AWS choose a supported default for this region/instance class."
  type        = string
  default     = null
  nullable    = true
}

variable "db_publicly_accessible" {
  description = "Whether the RDS instance is temporarily exposed with a public endpoint for connectivity drills. Keep false by default."
  type        = bool
  default     = false
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
  engine_version          = var.db_engine_version
  instance_class          = var.db_instance_class
  allocated_storage       = 20
  db_name                 = var.db_name
  username                = var.db_username
  password                = var.db_password
  db_subnet_group_name    = aws_db_subnet_group.devtest.name
  vpc_security_group_ids  = [local.effective_db_security_group_id]
  publicly_accessible     = var.db_publicly_accessible
  skip_final_snapshot     = true
  deletion_protection     = false
  backup_retention_period = 0

  lifecycle {
    precondition {
      condition     = local.effective_db_security_group_id != null
      error_message = "Provide db_security_group_id (preferred) or legacy db_sg_id for the RDS instance security group."
    }
  }

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
