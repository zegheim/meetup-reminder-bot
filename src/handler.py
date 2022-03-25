import os
from datetime import date, datetime, timedelta

import pytz
from aws_lambda_typing import context, events

from src.lib.bot import MeetupReminderBot

NEXT_WEEK = date.today() + timedelta(days=7)
NEXT_WEEK = date(2022, 3, 28)


def is_reminder_time() -> bool:
    today = datetime.now().astimezone(pytz.timezone(os.environ["MEETUP_EVENT_TZ"]))
    return today.hour == int(os.environ["MEETUP_EVENT_HOUR_24H"])


def lambda_handler(event: events.EventBridgeEvent, context_: context.Context):
    if not is_reminder_time():
        return {"message": "Not reminder time yet"}

    bot = MeetupReminderBot(os.environ["TG_BOT_TOKEN"], os.environ["TG_CHAT_ID"])
    message = bot.send_reminder(os.environ["MEETUP_GROUP_NAME"], NEXT_WEEK)

    return {"message": message.text}
