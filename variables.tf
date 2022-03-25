variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "bucket_prefix" {
  description = "Prefix for the bucket that will contain the Lambda deployment package"
  type        = string
}

variable "lambda_execution_role_prefix" {
  description = "Prefix for the Lambda function's execution role"
  type        = string
  validation {
    condition     = length(var.lambda_execution_role_prefix) >= 1 && length(var.lambda_execution_role_prefix) <= 38
    error_message = "The prefix of the Lambda's execution role must be no more than 38 characters."
  }
}

variable "lambda_handler" {
  description = "Entrypoint for the Lambda function"
  type        = string
}

variable "lambda_name" {
  description = "Name of the Lambda function"
  type        = string
}

variable "lambda_runtime" {
  description = "What language and version to run Lambda function in"
  type        = string
}

variable "object_name" {
  description = "Name of the Lambda deployment package in S3"
  type        = string
}
