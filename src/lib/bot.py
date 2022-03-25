from datetime import date

from src.lib.parser import MeetupEvent, get_event
from telegram import Bot, ChatAction, Message, ParseMode

DATE_FORMAT = "%A, %-d %B %Y %-I:%M %p"  # e.g. Monday, 7 March 2022 7:00 PM
REMINDER_TEMPLATE = """
Please RSVP to the following event:
    
<b>Event:</b> <a href="{url}">{title}</a>
<b>Date:</b> {date}

This has been a \U00002728 <i>public service announcement</i> \U00002728
"""


class MeetupReminderBot:
    def __init__(self, token: str, chat_id: str):
        self.bot = Bot(token=token)
        self.chat_id = chat_id

    @staticmethod
    def craft_reminder(event: MeetupEvent) -> str:
        return REMINDER_TEMPLATE.format(
            url=event.url, title=event.title, date=event.date.strftime(DATE_FORMAT)
        )

    def send_reminder(self, group_name: str, event_date: date) -> Message:
        event = get_event(group_name, event_date)
        reminder = MeetupReminderBot.craft_reminder(event)

        self.bot.send_chat_action(chat_id=self.chat_id, action=ChatAction.TYPING)

        return self.bot.send_message(
            chat_id=self.chat_id, text=reminder, parse_mode=ParseMode.HTML
        )
