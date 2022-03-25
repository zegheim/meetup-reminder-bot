import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta

from httplib2 import Http
from icalevents.icalevents import events as icalevents
from icalevents.icalparser import Event


class NoEventFoundException(Exception):
    """For better semantics"""


class NoEventURLFoundException(Exception):
    """For better semantics"""


@dataclass
class MeetupEvent:
    title: str
    date: datetime
    url: str


def get_event_url(group_name: str, description: str) -> str:
    match = re.search(rf"https://www.meetup.com/{group_name}/events/\d+", description)

    if not match:
        raise NoEventURLFoundException(
            f"Could not find event url from description: {description}"
        )

    return match.group(0)


def get_event(group_name: str, event_date: date) -> MeetupEvent:
    events: list[Event] = icalevents(
        url=f"https://www.meetup.com/{group_name}/events/ical/",
        start=event_date,
        end=(event_date + timedelta(days=1)),
        http=Http(),  # disable caching
    )

    if not events:
        raise NoEventFoundException(f"No event found for {group_name} on {event_date}")

    event_url = get_event_url(group_name, events[0].description)

    return MeetupEvent(events[0].summary, events[0].start, event_url)
