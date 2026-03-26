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
  description = "AWS region for the stable self-hosted runner host"
  type        = string
  default     = "ap-southeast-2"
}

variable "instance_name" {
  description = "Name tag for the stable self-hosted runner host"
  type        = string
  default     = "wlv3-cloud-dev-runner"
}

variable "instance_type" {
  description = "EC2 instance type for the stable self-hosted runner host"
  type        = string
  default     = "t3.small"
}

variable "subnet_id" {
  description = "Public subnet ID where the runner host will live"
  type        = string
}

variable "security_group_ids" {
  description = "Existing security groups to attach to the runner host. Pass the cloud-dev basic SG here so the DB SG can trust this host by SG instead of public IP."
  type        = list(string)
}

variable "ssh_ingress_cidrs" {
  description = "Operator IPv4 CIDRs allowed to SSH into the runner host"
  type        = list(string)
  default     = []
}

variable "key_name" {
  description = "Optional EC2 key pair name for SSH access"
  type        = string
  default     = ""
}

variable "root_volume_size_gb" {
  description = "Root EBS volume size in GiB"
  type        = number
  default     = 30
}

variable "runner_bootstrap_user_data" {
  description = "Whether to install the baseline OS packages needed by the stable runner host"
  type        = bool
  default     = true
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_security_group" "runner_ssh" {
  name        = "${var.instance_name}-ssh"
  description = "SSH ingress for the stable self-hosted runner host"
  vpc_id      = data.aws_subnet.selected.vpc_id

  dynamic "ingress" {
    for_each = var.ssh_ingress_cidrs

    content {
      from_port   = 22
      to_port     = 22
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
    Name        = "${var.instance_name}-ssh"
    Project     = "wordloom-v3"
    Environment = "cloud-dev"
    Role        = "github-actions-runner"
  }
}

data "aws_subnet" "selected" {
  id = var.subnet_id
}

locals {
  runner_user_data_script = <<-EOT
#!/usr/bin/env bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y ca-certificates curl git jq tar unzip docker.io python3 python-is-python3
systemctl enable docker
systemctl start docker
EOT

  runner_user_data = var.runner_bootstrap_user_data ? local.runner_user_data_script : null
}

resource "aws_instance" "runner" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = var.subnet_id
  key_name                    = trimspace(var.key_name) != "" ? var.key_name : null
  associate_public_ip_address = true
  vpc_security_group_ids      = concat(var.security_group_ids, [aws_security_group.runner_ssh.id])
  user_data                   = local.runner_user_data

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }

  root_block_device {
    volume_size = var.root_volume_size_gb
    volume_type = "gp3"
    encrypted   = true
  }

  tags = {
    Name        = var.instance_name
    Project     = "wordloom-v3"
    Environment = "cloud-dev"
    Role        = "github-actions-runner"
  }
}

output "runner_instance_id" {
  description = "Instance ID of the stable self-hosted runner host"
  value       = aws_instance.runner.id
}

output "runner_public_ip" {
  description = "Public IPv4 of the stable self-hosted runner host"
  value       = aws_instance.runner.public_ip
}

output "runner_private_ip" {
  description = "Private IPv4 of the stable self-hosted runner host"
  value       = aws_instance.runner.private_ip
}

output "runner_ssh_command" {
  description = "Suggested SSH command for the stable self-hosted runner host"
  value       = "ssh ubuntu@${aws_instance.runner.public_ip}"
}

output "runner_attached_security_groups" {
  description = "Security groups attached to the stable self-hosted runner host"
  value       = aws_instance.runner.vpc_security_group_ids
}