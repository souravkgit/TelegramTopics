class Config(object):
    TOKEN = ""  # Get bot token from bot father
    BOT_USERNAME = ""  # Bot username
    OWNER_ID = "1608141072"
    OWNER_USERNAME = "goyalcompany"
    DEV_USERNAME = "PythonDeveloperHub"
    TOPIC_ID = -10000000000
    TOPIC_THREADS = {
        "general": 1,
        "error": 2,
        "updates": 25,
        "fun": 4,
    }


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
