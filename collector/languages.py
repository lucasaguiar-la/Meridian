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
    return [lang.strip().lower() for lang in settings.languages.split(",") if lang.strip()]
