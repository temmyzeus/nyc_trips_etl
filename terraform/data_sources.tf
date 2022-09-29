data "aws_caller_identity" "account_details" {}

data "archive_file" "zip_python_code" {
  type             = "zip"
  source_file      = "${path.module}/../lambda/index.py"
  output_path      = "${path.module}/../files/output.zip"
  output_file_mode = "0666"
}
