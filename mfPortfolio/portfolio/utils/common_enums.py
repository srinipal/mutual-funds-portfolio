from enum import Enum


class SIPFrequency(Enum):
    MONTHLY = "Monthly"
    QUARTERLY = "Quarterly"
    WEEKLY = "Weekly"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


