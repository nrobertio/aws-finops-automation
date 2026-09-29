variable "region" {
  type    = string
  default = "eu-central-1"
}

variable "alert_email" {
  type = string
}

variable "monthly_budget" {
  description = "Monthly cost budget in USD."
  type        = number
  default     = 500
}

variable "required_tags" {
  description = "Cost-allocation tags every resource should carry."
  type        = list(string)
  default     = ["Project", "Environment", "Owner", "CostCenter"]
}
