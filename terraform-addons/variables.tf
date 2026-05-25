variable "grafana_admin_password" {
  description = "The admin password for Grafana"
  type        = string
  sensitive   = true
}

variable "aws_region" {
  description = "AWS region for resources"
  type	      = string
  default     = "us-east-1"
}
