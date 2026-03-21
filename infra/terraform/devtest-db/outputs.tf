output "db_endpoint" {
  value       = "localhost"
  description = "Dev/test DB endpoint"
}

output "db_port" {
  value       = var.db_port
  description = "Dev/test DB port"
}

output "db_name" {
  value       = var.db_name
  description = "Dev/test DB name"
}
