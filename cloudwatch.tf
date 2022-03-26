data "aws_iam_policy_document" "cloudwatch_role_policy_document" {
  statement {
    effect    = "Allow"
    actions   = ["logs:CreateLogStream"]
    resources = [aws_cloudwatch_log_group.lambda_log_group.arn]
  }

  statement {
    effect    = "Allow"
    actions   = ["logs:PutLogEvents"]
    resources = ["${aws_cloudwatch_log_group.lambda_log_group.arn}:*"]
  }
}

resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${var.lambda_name}"
  retention_in_days = 7
}

resource "aws_iam_policy" "cloudwatch_policy" {
  name        = "meetup-reminder-bot-cloudwatch-policy"
  description = "Cloudwatch policy to allow ${aws_iam_role.lambda_exec_role.name} to access Cloudwatch"
  policy      = data.aws_iam_policy_document.cloudwatch_role_policy_document.json
}
