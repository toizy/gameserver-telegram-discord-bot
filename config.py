"""
    Модуль для загрузки конфигурации из config.json в коллекцию cfg
"""

import json

# Типы серверных сообщений
SMT_MIN = 0
SMT_CHAT = 0
SMT_DISCORD = 1
SMT_ECHO = 2
SMT_CHEAT = 3
SMT_MAX = 3

# Определяем структуру конфигурации как коллекцию
config = {
    'host': 'localhost',
    'port': 10000,
    'discord': {
        'enabled': True,
        'bot_token': 'your_discord_bot_token',
        'channels': [
            {
                'enabled': True,
                'channel_id': 1234567890123456789,
                'handler': None,
                'name': "",
                'channel_type': [SMT_CHAT, SMT_DISCORD]
            }
        ]
    },
    'telegram': {
        'enabled': True,
        'bot_token': 'your_telegram_bot_token',
        'channels': [
            {
                'enabled': True,
                'channel_id': -1234567890,
                'handler': None,
                'channel_type': [SMT_CHAT, SMT_DISCORD]
            }
        ]
    }
}


def save_config_to_json():
    """
    Функция сохраняет коллекцию config в json файл
    """
    with open('config.json', 'w') as json_file:
        json.dump(config, json_file, indent=4)


def load_config_from_json():
    """
    Функция загружает коллекцию config из json файла
    """
    try:
        with open('config.json', 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print("Ошибка: Файл config.json не найден.")
        return None
    except json.JSONDecodeError:
        print("Ошибка: Неверный формат JSON в файле config.json.")
        return None


# save_config_to_json()
cfg = load_config_from_json()
