# meetup-reminder-bot
[![codecov](https://codecov.io/gh/zegheim/meetup-reminder-bot/branch/master/graph/badge.svg?token=58J21L84XA)](https://codecov.io/gh/zegheim/meetup-reminder-bot) 

Serverless Telegram bot to remind you to RSVP to your next Meetup session! Powered by [AWS Lambda](https://aws.amazon.com/lambda/) and [Amazon EventBridge](https://aws.amazon.com/eventbridge/).

# Pre-requisites
- [Terraform](https://www.terraform.io/) (v.1.1.7 and above)
- [Amazon Web Services (AWS)](https://aws.amazon.com/) account with [CLI v2 installed](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
- [Telegram Bot account](https://core.telegram.org/bots)
- [Poetry](https://python-poetry.org/)

# Installation
- `git clone` this project
- `cd` into the project directory, and run `poetry install`.
- Run `terraform init`, followed by `terraform apply`. 
- Follow the prompts as instructed.
- To verify your installation, run `aws lambda invoke --function-name=$(terraform output -raw lambda_name) response.json` and inspect `response.json` using your favourite text editor. You should see something like 
```
{"message": "Not reminder hour yet"}
```
# Configuration

In general all configuration variables should be defined in `terraform.tfvars`, **except** the following variables:

* `tg_bot_token` - your Telegram bot token,
* `tg_chat_id` - Telegram chat ID to send reminders to, and
* `meetup_group_name` - The Meetup group identifier whose events you would like to be reminded of.

These three variables would have to be filled in each time you run `terraform plan` or `terraform apply`, for security reasons. They have also been marked as `sensitive`, so they would not appear in any of the Terraform state files.

## Changing the reminder frequency

The defaults provided by the checked-in version of `terraform.tfvars` will remind you of events 7 days in advance, every Monday, Wednesday, and Thursday at 18:57 UK time. The following configuration variables determine the frequency at which reminders are sent:

| Variable                          | Description                                                                                                                                                                                                                                                                                                                                                                                                 |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `reminder_frequency`              | This should be a [cron expression](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html#CronExpressions). Note that Amazon EventBridge uses UTC time zone. For regions with multiple timezones, set Hours field to all their values when converted back to UTC. The bot will make sure to only send the reminder at the correct timezone (with the help of the variables below). |
| `meetup_event_hour_24h`           | The event hour in 24h format (e.g. 19 if your event starts at 7PM). Used to make sure that the bot will only send the reminder once, at the desired hour.                                                                                                                                                                                                                                                   |
| `meetup_event_num_days_lookahead` | Number of days you want to be reminded of events in advance. This is useful for popular groups / events that pretty much sells out within the first couple of hours of registrations being open. Set this number to the number of days between the event being open for registration and the actual event date.                                                                                             |
| `meetup_event_tz`                 | Meetup event timezone (e.g. Europe/London). Supports all timezones returned by `pytz.all_timezones`. Used as a workaround for countries with different timezones depending on the time of the year (e.g. United Kingdom switches to BST around late March each year, and then back to GMT around late October).                                                                                             |

# Repository structure

* The entire `src` directory is packaged up into a `.zip` file and used as our Lambda function's source code.
* All utility scripts (e.g. for packaging dependencies, etc.) live under the `scripts` directory.
* Unit tests are located under the `tests` directory, with its sub-directory structure mimicking that of `src`.
