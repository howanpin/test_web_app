from enum import Enum, IntEnum

class WeekNumberEnum(IntEnum):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5
    SIXTH = 6

class MenuTypeEnum(Enum):
    HYPERTROPHY = "hypertrophy"
    POWER = "power"
    STRENGTH = "strength"