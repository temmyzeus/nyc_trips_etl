terraform {
  required_version = ">= 0.12"
  backend "local" {}
  required_providers {
    aws = {
      version = ">= 4.23.0"
      source  = "hashicorp/aws"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "2.2.0"
    }
  }
}

provider "aws" {
  region                   = var.region
  shared_config_files      = var.aws_config_path
  shared_credentials_files = var.aws_credentials_path
  profile                  = var.profile
}
