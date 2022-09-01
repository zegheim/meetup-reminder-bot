data "aws_iam_policy_document" "lambda_assume_role_policy_document" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_exec_role" {
  name               = "${var.project_name}-lambda-execution-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy_document.json
}

resource "aws_iam_role_policy_attachment" "lambda_logging_to_cloudwatch" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "meetup_reminder_bot" {
  function_name    = var.lambda_name
  description      = var.project_description
  filename         = data.archive_file.lambda_zip.output_path
  runtime          = var.lambda_runtime
  handler          = var.lambda_handler
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  role             = aws_iam_role.lambda_exec_role.arn
  layers           = [aws_lambda_layer_version.meetup_reminder_bot.arn]

  depends_on = [
    aws_iam_role_policy_attachment.lambda_logging_to_cloudwatch
  ]

  environment {
    variables = {
      TG_BOT_TOKEN                    = var.tg_bot_token
      TG_CHAT_ID                      = var.tg_chat_id
      MEETUP_EVENT_HOUR_24H           = var.meetup_event_hour_24h
      MEETUP_EVENT_NUM_DAYS_LOOKAHEAD = var.meetup_event_num_days_lookahead
      MEETUP_EVENT_REGEX              = var.meetup_event_regex
      MEETUP_EVENT_TZ                 = var.meetup_event_tz
      MEETUP_GROUP_NAME               = var.meetup_group_name
      DEBUG_MODE                      = var.debug_mode ? "1" : ""
    }
  }
}

resource "aws_lambda_layer_version" "meetup_reminder_bot" {
  filename            = data.archive_file.layers_zip.output_path
  description         = "Contains all external dependencies needed for ${var.lambda_name} to run."
  layer_name          = "${var.lambda_name}-dependencies"
  compatible_runtimes = [var.lambda_runtime]
}
