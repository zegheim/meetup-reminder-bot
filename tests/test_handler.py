import os
from datetime import date, datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch

import pytz
from src.handler import is_reminder_hour, lambda_handler


class TestHandler(TestCase):
    @patch("src.handler.datetime")
    def test_is_reminder_hour(self, mock_datetime: MagicMock):
        mock_datetime.now.return_value = datetime(
            2022, 3, 26, 13, tzinfo=pytz.timezone("UTC")
        )

        self.assertTrue(is_reminder_hour("13", "UTC"))
        self.assertFalse(is_reminder_hour("13", "Asia/Jakarta"))

        self.assertFalse(is_reminder_hour("20", "UTC"))
        self.assertTrue(is_reminder_hour("20", "Asia/Jakarta"))

    @patch.dict(
        os.environ,
        {
            "TG_BOT_TOKEN": "1234567890:foobar",
            "TG_CHAT_ID": "12345678",
            "MEETUP_GROUP_NAME": "FooBar",
            "MEETUP_EVENT_HOUR_24H": "14",
            "MEETUP_EVENT_NUM_DAYS_LOOKAHEAD": "7",
            "MEETUP_EVENT_TZ": "Foo/Bar",
        },
    )
    @patch("src.handler.date", return_value=MagicMock())
    @patch("src.handler.MeetupReminderBot", return_value=MagicMock())
    def test_lambda_handler(self, mock_bot: MagicMock, mock_date: MagicMock):
        with patch("src.handler.is_reminder_hour", return_value=False):
            self.assertEqual(
                lambda_handler(MagicMock(), MagicMock())["message"],
                "Not reminder hour yet",
            )

        with patch(
            "src.handler.is_reminder_hour", return_value=True
        ) as mock_is_reminder_hour:
            mock_date.today.return_value = date(2022, 3, 26)
            lambda_handler(MagicMock(), MagicMock())
            mock_is_reminder_hour.assert_called_once_with("14", "Foo/Bar")
            mock_bot.assert_called_once_with("1234567890:foobar", "12345678")
            mock_bot.return_value.send_reminder.assert_called_once_with(
                "FooBar", date(2022, 4, 2)
            )
