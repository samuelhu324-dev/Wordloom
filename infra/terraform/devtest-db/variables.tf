variable "env" {
  type    = string
  default = "dev"
}

variable "db_name" {
  type    = string
  default = "wordloom_dev"
}

variable "db_port" {
  type    = number
  default = 5435
}
