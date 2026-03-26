# AWS Terraform playground (dev/test only)

This directory hosts AWS-focused Terraform modules for S4C (cloud dev/test infra & Terraform backbone).

- Scope: dev/test playground only, small resources that can be destroyed anytime.
- State: local `terraform.tfstate` files (ignored via `.gitignore`).
- Next steps:
  - Add `network/`, `devtest-db/`, `storage/` modules in later S4C phases.
  - Add `runner-host/` when S4D needs a stable cloud-resident self-hosted runner path.
