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

variable "public_subnet_b_cidr" {
  description = "CIDR block for the public subnet in ap-southeast-2b"
  type        = string
  default     = "10.42.1.0/24"
}

variable "db_subnet_a_cidr" {
  description = "CIDR block for the DB subnet in ap-southeast-2a"
  type        = string
  default     = "10.42.10.0/24"
}

variable "db_subnet_b_cidr" {
  description = "CIDR block for the DB subnet in ap-southeast-2b"
  type        = string
  default     = "10.42.11.0/24"
}

variable "allowed_postgres_cidrs" {
  description = "Temporary IPv4 CIDR allowlist for direct Postgres access during drills. Keep empty by default."
  type        = list(string)
  default     = []
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

resource "aws_subnet" "public_b" {
  vpc_id                  = aws_vpc.cloud_dev.id
  cidr_block              = var.public_subnet_b_cidr
  availability_zone       = "ap-southeast-2b"
  map_public_ip_on_launch = true

  tags = {
    Name        = "wlv3-cloud-dev-public-b"
    Project     = "wordloom-v3"
    Environment = "cloud-dev"
    Tier        = "public"
  }
}

resource "aws_internet_gateway" "cloud_dev" {
  vpc_id = aws_vpc.cloud_dev.id

  tags = {
    Name        = "wlv3-cloud-dev-igw"
    Project     = "wordloom-v3"
    Environment = "cloud-dev"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.cloud_dev.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.cloud_dev.id
  }

  tags = {
    Name        = "wlv3-cloud-dev-public-rt"
    Project     = "wordloom-v3"
    Environment = "cloud-dev"
  }
}

resource "aws_route_table_association" "public_a" {
  subnet_id      = aws_subnet.public_a.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_b" {
  subnet_id      = aws_subnet.public_b.id
  route_table_id = aws_route_table.public.id
}

resource "aws_subnet" "db_a" {
  vpc_id                  = aws_vpc.cloud_dev.id
  cidr_block              = var.db_subnet_a_cidr
  availability_zone       = "ap-southeast-2a"
  map_public_ip_on_launch = false

  tags = {
    Name        = "wlv3-cloud-dev-db-a"
    Project     = "wordloom-v3"
    Environment = "cloud-dev"
    Tier        = "db"
  }
}

resource "aws_subnet" "db_b" {
  vpc_id                  = aws_vpc.cloud_dev.id
  cidr_block              = var.db_subnet_b_cidr
  availability_zone       = "ap-southeast-2b"
  map_public_ip_on_launch = false

  tags = {
    Name        = "wlv3-cloud-dev-db-b"
    Project     = "wordloom-v3"
    Environment = "cloud-dev"
    Tier        = "db"
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

resource "aws_security_group" "db" {
  name        = "wlv3-cloud-dev-sg-db"
  description = "DB security group for wordloom-v3 dev/test"
  vpc_id      = aws_vpc.cloud_dev.id

  # 先只允许来自基础 dev/test SG 的 Postgres 流量。
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.cloud_dev_basic.id]
  }

  dynamic "ingress" {
    for_each = var.allowed_postgres_cidrs

    content {
      from_port   = 5432
      to_port     = 5432
      protocol    = "tcp"
      cidr_blocks = [ingress.value]
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "wlv3-cloud-dev-sg-db"
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

output "public_subnet_ids" {
  description = "IDs of the public subnets across two AZs"
  value       = [aws_subnet.public_a.id, aws_subnet.public_b.id]
}

output "basic_sg_id" {
  description = "ID of the basic dev/test security group"
  value       = aws_security_group.cloud_dev_basic.id
}

output "db_subnet_ids" {
  description = "IDs of the DB subnets for the dev/test RDS subnet group"
  value       = [aws_subnet.db_a.id, aws_subnet.db_b.id]
}

output "db_sg_id" {
  description = "ID of the DB security group"
  value       = aws_security_group.db.id
}

output "allowed_postgres_cidrs" {
  description = "Temporary IPv4 CIDR allowlist configured for direct Postgres access"
  value       = var.allowed_postgres_cidrs
}
