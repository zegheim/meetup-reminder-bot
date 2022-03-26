from datetime import date, datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.lib.bot import MeetupReminderBot
from src.lib.parser import MeetupEvent
from telegram import ChatAction, ParseMode


class TestBot(TestCase):
    def setUp(self):
        self.event = MeetupEvent(
            "Foo bar", datetime(2022, 3, 26, 1, 2, 3), "https://www.example.com"
        )

    def test_craft_reminder(self):
        reminder = MeetupReminderBot.craft_reminder(self.event)
        self.assertIn("Foo bar", reminder)
        self.assertIn("Saturday, 26 March 2022 1:02 AM", reminder)
        self.assertIn("https://www.example.com", reminder)

    @patch.object(MeetupReminderBot, "craft_reminder", return_value="My reminder")
    @patch("src.lib.bot.get_event")
    def test_send_reminder(self, mock_get_event: MagicMock, *args):
        mock_get_event.return_value = self.event
        bot = MeetupReminderBot("1234567890:foobar", "12345678")

        with patch.object(
            bot.bot, "send_chat_action"
        ) as mock_send_chat_action, patch.object(
            bot.bot, "send_message"
        ) as mock_send_message:
            bot.send_reminder("FooBarBaz", date(2022, 3, 26))
            mock_send_chat_action.assert_called_with(
                chat_id="12345678", action=ChatAction.TYPING
            )
            mock_send_message(
                chat_id="12345678", text="My reminder", parse_mode=ParseMode.HTML
            )
