output "lambda_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.meetup_reminder_bot.function_name
}
