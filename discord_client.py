# Модуль для работы с Discord API и отправки сообщений
import discord
from discord.ext import commands

# Подключаем конфигурацию
from config import cfg
from logger import log
from server_communications import send_message_to_gs

# Создаем клиента Discord
intents = discord.Intents.all()
intents.typing = False
intents.presences = False
intents.messages = True  # Включаем намерения для получения сообщений

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    """
    Обработчик подключения бота к Discord
    """
    log.info("-----------------------------")
    log.info("---- Каналы Discord бота ----")
    log.info("-----------------------------")
    # Находим текстовый канал для отправки сообщений
    for guild in bot.guilds:
        for channel in guild.channels:
            log.info(f'{channel}: {channel.id}')
            for item in cfg['discord']['channels']:
                if channel.id == item['channel_id']:
                    item['handle'] = channel
                    item['name'] = channel
                    break

    log.info("-----------------------------")

    # Проверяем, были ли найдены необходимые каналы
    for channel in cfg['discord']['channels']:
        if channel['enabled'] and channel['handle']:
            log.info(f'Required channel: {channel["name"]}: {channel["channel_id"]}.')


@bot.event
async def on_message(message):
    """
    Обработчик сообщения, полученного из группы Discord
    :param message: Объект сообщения
    """
    # Сообщение от бота, выходим
    if message.author == bot.user:
        return

    channel = None

    # Перебираем идентификаторы каналов из config.discord.channels
    for item in cfg['discord']['channels']:
        if item['enabled'] and message.channel.id == item['channel_id']:
            channel = item['handle']
            break

    if not channel:
        return

    # Отправляем стикер
    if message.content.startswith('!'):
        await message.channel.send(f"{message.author.name}", file=discord.File(f"./img/{message.content}.webp"))
        await message.delete()
        return
    else:
        await send_message_to_gs(message.author.name, message.clean_content)


async def discord_bot_start():
    """
    Функция, запускающая Discord бота (асинхронно)
    """
    try:
        await bot.start(cfg['discord']['bot_token'])
    except KeyboardInterrupt:
        pass
    finally:
        await bot.close()
