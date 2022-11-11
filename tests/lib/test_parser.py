from datetime import date, datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch

from icalevents.icalparser import Event
from src.lib.parser import (
    NoEventFoundException,
    NoEventURLFoundException,
    get_event,
    get_event_url,
)


def create_event(summary: str, start: datetime) -> Event:
    """Helper function to create test events

    Parameters
    ----------
    summary : str
        Event summary
    start : datetime
        Event start time

    Returns
    -------
    Event
        Test event
    """
    event = Event()
    event.summary = summary
    event.start = start
    return event


class TestParser(TestCase):
    def setUp(self):
        self.group_name = "FooBarBaz"

    def test_get_event_url_description_contains_url(self):
        description = "foo bar baz \n https://www.meetup.com/FooBarBaz/events/1234567890/ foobar \n foobaz"
        self.assertEqual(
            get_event_url(self.group_name, description),
            "https://www.meetup.com/foobarbaz/events/1234567890/",
        )

    def test_get_event_url_description_contains_url_case_insensitive(self):
        description = "foo bar baz \n https://www.meetup.com/foobarbaz/events/1234567890/ foobar \n foobaz"
        self.assertEqual(
            get_event_url(self.group_name, description),
            "https://www.meetup.com/foobarbaz/events/1234567890/",
        )

    def test_get_event_url_description_contains_no_url(self):
        description = "foo bar baz \n https://www.example.com/ foobar \n foobaz"
        with self.assertRaises(NoEventURLFoundException):
            get_event_url(self.group_name, description)

    @patch("src.lib.parser.get_event_url", return_value="https://www.example.com/")
    def test_get_event_no_regex(self, mock_get_event_url: MagicMock):
        with patch("src.lib.parser.icalevents", return_value=[]):
            with self.assertRaises(NoEventFoundException):
                get_event(self.group_name, date(2022, 3, 26))

        expected_event = Event()
        expected_event.summary = "Foo bar"
        expected_event.start = datetime(2022, 3, 26, 1, 2, 3)

        with patch("src.lib.parser.icalevents", return_value=[expected_event, Event()]):
            event = get_event(self.group_name, date(2022, 3, 26))
            mock_get_event_url.assert_called_with(self.group_name, None)
            self.assertEqual(event.title, expected_event.summary)
            self.assertEqual(event.date, expected_event.start)
            self.assertEqual(event.url, "https://www.example.com")

    @patch("src.lib.parser.get_event_url", return_value="https://www.example.com")
    def test_get_event_with_regex(self, mock_get_event_url: MagicMock):
        event_1 = create_event("Foo bar", datetime(2022, 3, 26, 1, 2, 3))
        event_2 = create_event("Foo baz", datetime(2022, 3, 26, 1, 2, 3))

        with patch("src.lib.parser.icalevents", return_value=[event_1, event_2]):
            with self.assertRaises(NoEventFoundException):
                get_event(self.group_name, date(2022, 3, 26), event_regex=r"Bar baz")

        with patch("src.lib.parser.icalevents", return_value=[event_2, event_1]):
            event = get_event(
                self.group_name, date(2022, 3, 26), event_regex=r"(:?Foo bar|Bar baz)"
            )
            mock_get_event_url.assert_called_with(self.group_name, None)
            self.assertEqual(event.title, event_1.summary)
            self.assertEqual(event.date, event_1.start)
            self.assertEqual(event.url, "https://www.example.com")
