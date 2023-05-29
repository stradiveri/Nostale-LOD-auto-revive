import configparser

settings = configparser.ConfigParser()
settings.read('char_settings.ini', encoding="utf-8")

class user_settings:
    characters = settings["character_settings"]["characters"]
    min_delay = settings["revive_delays"]["revive_min(seconds)"]
    max_delay = settings["revive_delays"]["revive_max(seconds)"]
