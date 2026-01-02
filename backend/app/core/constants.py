from enum import Enum


class UserRole(str, Enum):
    PARENT = "parent"
    ADMIN = "admin"


class LanguageCode(str, Enum):
    EN = "en"
    PL = "pl"
    ES = "es"


class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class ProgressStatus(str, Enum):
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    IN_PROGRESS = "in_progress"
    PRACTICING = "practicing"
    MASTERED = "mastered"


LANGUAGE_NAMES = {
    LanguageCode.EN: "English",
    LanguageCode.PL: "Polish",
    LanguageCode.ES: "Spanish",
}
