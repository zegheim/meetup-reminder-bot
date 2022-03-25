
#--------------------------------------------------------------
# AWS General
#--------------------------------------------------------------
aws_profile = "default"
aws_region  = "eu-west-2"

#--------------------------------------------------------------
# AWS S3 
#--------------------------------------------------------------
bucket_prefix = "terraform-meetup-reminder-bot-"
object_name   = "meetup-reminder-bot"

#--------------------------------------------------------------
# AWS Lambda
#--------------------------------------------------------------

lambda_execution_role_prefix = "terraform-lambda-execution-role-"
lambda_handler               = "handler.lambda_handler"
lambda_name                  = "MeetupReminderBot"
lambda_runtime               = "python3.9"


