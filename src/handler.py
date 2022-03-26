import os
from datetime import date, datetime, timedelta

import pytz
from aws_lambda_typing import context, events

from src.lib.bot import MeetupReminderBot

NEXT_WEEK = date.today() + timedelta(days=7)


def is_reminder_hour(event_hour: str, event_tz: str) -> bool:
    """Checks if it is time to send the reminder yet.

    Parameters
    ----------
    event_hour : str
        Meetup event hour (in 24h format, e.g. "18")
    event_tz : str
        Meetup event timezone (e.g. "Europe/London")

    Returns
    -------
    is_reminder_hour : bool
        True if it is time to send reminder, else False
    """
    today = datetime.now().astimezone(pytz.timezone(event_tz))
    return today.hour == int(event_hour)


def lambda_handler(event: events.EventBridgeEvent, context_: context.Context):
    """Entrypoint for our Lambda function.

    Parameters
    ----------
    event : events.EventBridgeEvent
        See https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-events.html
    context_ : context.Context
        See https://docs.aws.amazon.com/lambda/latest/dg/python-context.html

    Returns
    -------
    dict[str, str]
        Sent reminder message, or "Not reminder hour yet"
    """
    if not is_reminder_hour(
        os.environ["MEETUP_EVENT_HOUR_24H"], os.environ["MEETUP_EVENT_TZ"]
    ):
        return {"message": "Not reminder hour yet"}

    bot = MeetupReminderBot(os.environ["TG_BOT_TOKEN"], os.environ["TG_CHAT_ID"])
    message = bot.send_reminder(os.environ["MEETUP_GROUP_NAME"], NEXT_WEEK)

    return {"message": message.text}
