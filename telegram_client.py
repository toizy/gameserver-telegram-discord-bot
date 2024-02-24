"""
    Модуль для работы с Telegram API
"""

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message

from config import cfg
from logger import log
from server_communications import send_message_to_gs

# Инициализируем бота и диспетчера
bot = Bot(token=cfg['telegram']['bot_token'])
dp = Dispatcher()


async def telegram_send_message(chat_id, text):
    """
    Функция отправки сообщения в группу Телеграм
    :param chat_id: Идентификатор чата
    :param text:  Текст сообщения
    """
    await bot.send_message(chat_id=chat_id, text=text)


@dp.message()
async def echo(message: Message):
    """
    Принимает сообщение из группы Телеграм и перенаправляет его серверу через сокет
    :param message: Объект сообщения от бота
    """
    if not message.from_user.is_bot:
        await send_message_to_gs(message.from_user.username, message.text)


async def telegram_bot_start():
    """
    Функция, запускающая Телеграм бота (асинхронно)
    """
    log.info('Телеграм бот запускается...')

    # Сохраняем ссылку на функцию 'send_message'
    for item in cfg['telegram']['channels']:
        item['handle'] = telegram_send_message

    try:
        await dp.start_polling(bot)
    except ValueError as e:
        log.error(f'Запуск бота завершился ошибкой: {e}')
    except asyncio.CancelledError:
        log.info('Телеграм бот остановлен.')
    except KeyboardInterrupt:
        pass
    finally:
        await bot.close()
        await dp.storage.close()
