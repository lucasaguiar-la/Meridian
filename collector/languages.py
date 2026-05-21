from config.settings import settings

SUPPORTED_LANGUAGES = [
    "python",
    "javascript",
    "typescript",
    "go",
    "rust",
    "java",
    "c++",
    "c#",
    "kotlin",
    "swift",
]


def get_active_languages() -> list[str]:
    return [lang.lower() for lang in settings.languages]
