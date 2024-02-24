"""
    Модуль для коммуникации ботов с игровым сервером через сокеты.
"""

import asyncio
import socket
import struct
import uuid

from config import cfg, SMT_ECHO
from logger import log
from utils import check_server_message_type

# Сокет
server_socket = None
client_socket = None


async def receive_data(sock):
    while True:
        try:
            # Получаем данные от сервера
            data = await asyncio.get_event_loop().sock_recv(sock, 1024)
            if not data:
                break

            # Выводим данные в бинарном виде
            # print("Received:", data)

            # Получаем тип и текст сообщения
            msg_type = data[0]
            if check_server_message_type(msg_type):
                msg_text = data[3:data.index(0, 3)].decode('windows-1251')

                # Echo-сообщение - форматируем в Markdown
                if msg_type == SMT_ECHO:
                    msg_text = f'**{msg_text}**'

                # Перенаправляем данные в каналы Discord
                for item in cfg['discord']['channels']:
                    if item['enabled'] and msg_type in item['channel_type']:
                        await item['handle'].send(msg_text)

                # Перенаправляем данные в каналы Telegram
                for item in cfg['telegram']['channels']:
                    if item['enabled'] and msg_type in item['channel_type']:
                        await item['handle'](item['channel_id'], msg_text)

        except ConnectionResetError:
            log.warning("Клиент сбросил соединение")
            break


async def send_data(sock, message_bytes):
    try:
        await asyncio.get_event_loop().sock_sendall(sock, message_bytes)
    except ConnectionResetError:
        log.warning("Клиент сбросил соединение")


async def handle_client(client_sock, client_addr):
    log.info(f"Установлено соединение: {client_addr}")
    try:
        # Получаем и выводим данные от сервера
        await receive_data(client_sock)
    finally:
        # Закрываем соединение
        if client_socket is not None:
            client_socket.close()


async def send_message_to_gs(author, content):
    # global client_socket

    if author is None or len(author) == 0 or content is None or len(content) == 0:
        return

    message_id = str(uuid.uuid4())

    author_bytes = author.encode('windows-1251')
    content_bytes = content.encode('windows-1251')
    message_id_bytes = message_id.encode('windows-1251')

    # Формируем пакет данных для отправки на сервер игры
    message_length = len(author_bytes) + 1 + len(content_bytes) + 1 + len(message_id) + 1
    packet = \
        struct.pack('>BH', SMT_ECHO, message_length) + \
        struct.pack(f'<{len(content_bytes)}s', content_bytes) + b'\x00' + \
        struct.pack(f'<{len(author_bytes)}s', author_bytes) + b'\x00' + \
        struct.pack(f'<{len(message_id_bytes)}s', message_id_bytes) + b'\x00'

    # print('Packet in bytes:', packet.hex())

    await send_data(client_socket, packet)


async def create_socket():
    global server_socket, client_socket
    while True:
        try:
            # Создаем сокет
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Привязываем сокет к адресу и порту
            server_address = (cfg['host'], cfg['port'])
            server_socket.bind(server_address)

            # Слушаем входящие подключения
            server_socket.listen(1)

            log.info("Ожидаю подключения к сокету...")

            while True:
                # Принимаем входящее подключение
                client_socket, client_address = await asyncio.get_event_loop().sock_accept(server_socket)
                await handle_client(client_socket, client_address)
        except OSError as e:
            log.error(f"Возникла ошибка при создании сокета: {e}")
            if server_socket is not None:
                server_socket.close()
            log.info('Повтор через 10 секунд...')
            await asyncio.sleep(10)
        except KeyboardInterrupt:
            pass
