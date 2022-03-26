resource "aws_cloudwatch_event_rule" "reminder_schedule" {
  name                = "${var.project_name}-reminder-schedule"
  description         = "Determines when to send reminders"
  schedule_expression = var.eventbridge_schedule_expression
}

resource "aws_cloudwatch_event_target" "attach_reminder_schedule_to_lambda" {
  arn  = aws_lambda_function.meetup_reminder_bot.arn
  rule = aws_cloudwatch_event_rule.reminder_schedule.name
}

resource "aws_lambda_permission" "allow_eventbridge" {
  action        = "lambda:invokeFunction"
  function_name = aws_lambda_function.meetup_reminder_bot.function_name
  principal     = "events.amazonaws.com"
  statement_id  = "AllowEventBridgeToInvokeLambda"
  source_arn    = aws_cloudwatch_event_rule.reminder_schedule.arn
}