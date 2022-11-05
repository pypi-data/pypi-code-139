"""Date handling."""
import random
from datetime import datetime


DAYS = [
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
  "Sunday",
]


class DoomsDate:
    """A custom date implementation."""

    def __init__(self, year: int, month: int, day: int) -> None:
        """Initialize object."""
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def random(cls, start, end):
        """Return a random DoomsDate between start and end (inclusive)."""
        dt_start = datetime(start.year, start.month, start.day)
        dt_end = datetime(end.year, end.month, end.day)
        dt_random = dt_start + (dt_end - dt_start) * random.random()
        return DoomsDate(dt_random.year, dt_random.month, dt_random.day)

    def weekday(self) -> int:
        """Return numerical weekday."""
        return datetime(self.year, self.month, self.day).weekday()

    def __str__(self) -> str:
        """Return string representation (YYYY-mm-dd)."""
        return f"{self.year}-{self.month:02}-{self.day:02}"
