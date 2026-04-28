variable "bucket_name" {
  type        = string
  description = "Globally unique name for the site bucket"
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "domain_name" {
  type        = string
  description = "Full domain for the resume site"
}

variable "github_repo" {
  type        = string
  description = "GitHub repo in owner/name format"
}