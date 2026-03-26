# AWS stable runner host module (S4D-4C / P1-C1-S1)

This module provisions a small cloud-dev EC2 host intended to run the stable GitHub Actions self-hosted runner for S4D cloud release operations.

Why this exists:

- The previous dispatch path proved that the workflow itself can PASS, but it still depended on temporary public-IP allowlists.
- The cloud-dev DB security group already trusts the cloud-dev basic security group.
- A runner host attached to that security group removes the need to keep chasing operator or target public IP drift.

Intended use:

1. Apply the network module first and capture:
   - `public_subnet_id`
   - `basic_sg_id`
2. Fill in `terraform.tfvars` for this module.
3. `terraform init`
4. `terraform apply`
5. SSH into the instance and complete GitHub runner registration via `scripts/ops/cloud_stable_runner_bootstrap.sh`.

Notes:

- This module only provisions the host and baseline OS packages. It does not embed GitHub registration tokens or repo secrets into Terraform state.
- Keep this dev/test only. The host is meant to be replaceable.