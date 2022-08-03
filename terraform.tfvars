
#--------------------------------------------------------------
# Project specific
#--------------------------------------------------------------

project_name                    = "meetup-reminder-bot"
project_description             = "Telegram bot to remind you to RSVP to your next Meetup session!"
meetup_event_hour_24h           = 18
meetup_event_num_days_lookahead = 7
meetup_event_tz                 = "Europe/London"

#--------------------------------------------------------------
# AWS General
#--------------------------------------------------------------

aws_profile = "default"
aws_region  = "eu-west-2"

#--------------------------------------------------------------
# AWS Lambda
#--------------------------------------------------------------

lambda_name = "MeetupReminderBot"

#--------------------------------------------------------------
# AWS EventBridge
#--------------------------------------------------------------

reminder_frequency = "cron(57, 17,18 ? * MON,WED,THU *)"
