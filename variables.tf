variable "aws_profile" {
  description = "AWS CLI profile to use (see ~/.aws/config)"
  type        = string
  default     = "default"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "reminder_frequency" {
  description = "Determines the frequency at which the bot will send you reminders. See https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html for more information"
  type        = string
}

variable "lambda_handler" {
  description = "Entrypoint for the Lambda function"
  type        = string
  default     = "src.handler.lambda_handler"
}

variable "lambda_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "MeetupReminderBot"
}

variable "lambda_runtime" {
  description = "What language and version to run Lambda function in"
  type        = string
  default     = "python3.9"
}

variable "meetup_event_hour_24h" {
  description = "Meetup event hour you would like to be notified for (24h format)"
  type        = number

  validation {
    condition     = var.meetup_event_hour_24h >= 0 && var.meetup_event_hour_24h <= 23
    error_message = "The meetup_event_hour_24h value must be a number between 0 and 23."
  }
}

variable "meetup_event_num_days_lookahead" {
  description = "Number of days you would like to be reminded for events in advance"
  type        = number
}

variable "meetup_event_tz" {
  description = "Meetup event timezone"
  type        = string
}

variable "meetup_group_name" {
  description = "Meetup group identifier whose events you would like to be reminded of"
  type        = string
  sensitive   = true
}

variable "project_name" {
  description = "Name of this project. Used across the codebase as identifiers"
  type        = string
  default     = "meetup-reminder-bot"
}

variable "project_description" {
  description = "One sentence summary of this project. Used across the codebase as identifiers"
  type        = string
  default     = "Telegram bot to remind you to RSVP to your next Meetup session!"
}

variable "tg_bot_token" {
  description = "Telegram bot token. See https://core.telegram.org/bots/api#authorizing-your-bot for more information"
  type        = string
  sensitive   = true
}

variable "tg_chat_id" {
  description = "Telegram chat ID to send reminders to. See https://core.telegram.org/bots/api#chat for more info"
  type        = string
  sensitive   = true
}
