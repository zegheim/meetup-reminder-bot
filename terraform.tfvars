
#--------------------------------------------------------------
# Project specific
#--------------------------------------------------------------

project_name                    = "meetup-reminder-bot-lebc-coaching"
project_description             = "Telegram bot to remind you to RSVP to your next LEBC coaching session!"
meetup_event_hour_24h           = 17
meetup_event_num_days_lookahead = 27
meetup_event_regex              = "LEBC - Badminton Coaching Session - Friday at 7pm"
meetup_event_tz                 = "Europe/London"
meetup_group_name               = "london-east-badminton-club"

#--------------------------------------------------------------
# AWS General
#--------------------------------------------------------------

aws_profile = "default"
aws_region  = "eu-west-2"

#--------------------------------------------------------------
# AWS Lambda
#--------------------------------------------------------------

lambda_name = "MeetupReminderBot-LEBCCoachingFri7pm"

#--------------------------------------------------------------
# AWS EventBridge
#--------------------------------------------------------------

reminder_frequency = "cron(57 16,17 ? * FRI *)"
