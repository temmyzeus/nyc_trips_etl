variable "profile" {
  type        = string
  default     = "default"
  description = "AWS Profile"
}

variable "region" {
  type        = string
  default     = "us-west-2"
  description = "AWS Resource Region"
}

variable "aws_config_path" {
  type        = tuple([string])
  default     = ["$HOME/.aws/config"]
  description = "AWS Configuration Path"
}

variable "aws_credentials_path" {
  type        = tuple([string])
  default     = ["$HOME/.aws/credentials"]
  description = "AWS Credentials Path"
}

variable "bucket_prefix" {
  type        = string
  description = "Name of bucket to be appended to Account ID"
}

variable "function_name" {
  type        = string
  description = "Name of Lambda Function"
}