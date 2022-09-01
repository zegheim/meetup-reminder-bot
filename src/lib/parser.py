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
    """Retrieves the event URL from the event description.

    Parameters
    ----------
    group_name : str
        Meetup group name, used to detect event URL
    description : str
        Meetup event description to look for event URL in

    Returns
    -------
    event_url : str
        The retrieved event URL from the given event description

    Raises
    ------
    NoEventURLFoundException
        Raised if no event URL can be found from the given event description
    """
    match = re.search(
        rf"https://www.meetup.com/{group_name.lower()}/events/\d+", description.lower()
    )

    if not match:
        raise NoEventURLFoundException(
            f"Could not find event url from description: {description.lower()}"
        )

    return match.group(0)


def get_event(
    group_name: str, event_date: date, event_regex: str = ".*"
) -> MeetupEvent:
    """Retrieves the first event matching `event_regex` for `group_name` happening on `event_date`.

    Parameters
    ----------
    group_name : str
        Meetup group name to look for events in
    event_date : date
        Date to look for events in
    event_regex : str, optional
        Regular expression to optionally filter events by
        Defaults to ".*" (matches all events)

    Returns
    -------
    meetup_event : MeetupEvent
        The first event matching `event_regex` organised by `group_name`, hosted on `event_date`

    Raises
    ------
    NoEventFoundException
        Raised if no event matching `event_regex` is organised by `group_name` on `event_date`
    """
    events: list[Event] = icalevents(
        url=f"https://www.meetup.com/{group_name}/events/ical/",
        start=event_date,
        end=(event_date + timedelta(days=1)),
        http=Http(),  # disable caching
    )

    try:
        event = next(event for event in events if re.match(event_regex, event.summary))
    except StopIteration:
        raise NoEventFoundException(
            f"No event matching {event_regex} found for {group_name} on {event_date}"
        )

    event_url = get_event_url(group_name, event.description)

    return MeetupEvent(event.summary, event.start, event_url)
