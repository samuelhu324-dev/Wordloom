terraform {
  required_version = ">= 1.5.0"
}

# v1 skeleton: use null_resource to capture desired devtest DB state without
# actually provisioning cloud resources. Future phases can replace this with a
# real DB resource (e.g. aws_db_instance / azurerm_postgresql_flexible_server).
resource "null_resource" "devtest_db" {
  triggers = {
    env     = var.env
    db_name = var.db_name
    db_port = var.db_port
  }
}
