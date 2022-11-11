#--------------------------------------------------------------	
# Project specific	
#--------------------------------------------------------------	

project_name                    = "meetup-reminder-bot-lsbc"
project_description             = "Telegram bot to remind you to RSVP to your next LSBC session!"
meetup_event_hour_24h           = 18
meetup_event_num_days_lookahead = 7
meetup_event_regex              = "(?:MON|WED|THU) @ Stratford Chobham Academy \\([23] hrs\\) \\((?:All Levels|ADVANCED Level)\\)"
meetup_event_tz                 = "Europe/London"
meetup_group_name               = "londonsocialbadminton"

#--------------------------------------------------------------	
# AWS General	
#--------------------------------------------------------------	

aws_profile = "default"
aws_region  = "eu-west-2"

#--------------------------------------------------------------	
# AWS Lambda	
#--------------------------------------------------------------	

lambda_name = "MeetupReminderBot-LSBCMonWedThu7pm"

#--------------------------------------------------------------	
# AWS EventBridge	
#--------------------------------------------------------------	

reminder_frequency = "cron(57 17,18 ? * MON,WED,THU *)"
