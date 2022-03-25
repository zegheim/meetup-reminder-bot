
#--------------------------------------------------------------
# Project specific
#--------------------------------------------------------------

project_name        = "meetup-reminder-bot"
project_description = "Telegram bot to remind you to RSVP to your next Meetup session!"

#--------------------------------------------------------------
# AWS General
#--------------------------------------------------------------

aws_profile = "default"
aws_region  = "eu-west-2"

#--------------------------------------------------------------
# AWS Lambda
#--------------------------------------------------------------

lambda_execution_role_prefix = "terraform-lambda-execution-role-"
lambda_handler               = "src.handler.lambda_handler"
lambda_name                  = "MeetupReminderBot"
lambda_runtime               = "python3.9"

meetup_event_hour_24h = 19
meetup_event_tz       = "Europe/London"

#--------------------------------------------------------------
# AWS EventBridge
#--------------------------------------------------------------

eventbridge_schedule_expression = "cron(0 18,19 ? * MON,THU *)"
