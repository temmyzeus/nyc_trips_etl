data "aws_caller_identity" "account_details" {}

data "archive_file" "zip_python_code" {
  type             = "zip"
  source_file      = local.lambda_source_file
  output_path      = "${path.module}/../files/output-${random_uuid.output_uuid.result}.zip"
  output_file_mode = "0666"
}
