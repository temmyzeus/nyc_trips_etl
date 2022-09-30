resource "aws_s3_bucket" "bucket" {
  bucket = "${var.bucket_prefix}-${data.aws_caller_identity.account_details.account_id}"
  tags = {
    Project = "Nyc-Taxis"
  }
}

resource "aws_iam_role" "lambda_role" {
  name        = "NYC_Lambda_function_role"
  description = "Lambda functions to download NYC Trips data"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "",
        "Effect" : "Allow",
        "Principal" : {
          "Service" : "lambda.amazonaws.com"
        },
        "Action" : "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_lambda_function" "nyc_lambda_function" {
  function_name = var.function_name
  role          = aws_iam_role.lambda_role.arn
  runtime       = "python3.9"
  filename      = "${path.module}/../files/output.zip"
  handler       = "index.lambda_handler"
}

resource "aws_iam_role_policy_attachment" "lambda_cloudwatch_attach_policy" {
  role       = aws_iam_role.lambda_role.id
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchLambdaInsightsExecutionRolePolicy"
}
