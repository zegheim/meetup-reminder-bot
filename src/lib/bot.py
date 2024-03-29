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
        """Populates `REMINDER_TEMPLATE` with metadata from `event`.

        Parameters
        ----------
        event : MeetupEvent
            Meetup event metadata to populate `REMINDER_TEMPLATE` with

        Returns
        -------
        reminder : str
            The reminder message to be sent
        """
        return REMINDER_TEMPLATE.format(
            url=event.url, title=event.title, date=event.date.strftime(DATE_FORMAT)
        )

    def send_reminder(
        self, group_name: str, event_date: date, event_regex: str = ".*"
    ) -> Message:
        """Sends reminder to RSVP to Meetup events.

        Parameters
        ----------
        group_name : str
            Meetup group name, used to find out the next event to RSVP to
        event_date : date
            Date for the next event to RSVP to
        event_regex : str, optional
            Regular expression to optionally filter events by
            Defaults to ".*" (matches all events)

        Returns
        -------
        message : Message
            Telegram message metadata
        """
        event = get_event(group_name, event_date, event_regex=event_regex)
        reminder = MeetupReminderBot.craft_reminder(event)

        self.bot.send_chat_action(chat_id=self.chat_id, action=ChatAction.TYPING)

        return self.bot.send_message(
            chat_id=self.chat_id, text=reminder, parse_mode=ParseMode.HTML
        )
