"""
    Программа позволяет игровому серверу отправлять сообщения в Discord и Telegram группы,
    а также получать сообщения из групп. Для этого сервер реализует сокет и простой протокол обмена
    сообщениями. Программа создаёт сокет, к которому сервер подключается и служит посредником.
"""
import asyncio
import signal

from discord_client import discord_bot_start
from server_communications import create_socket
from telegram_client import telegram_bot_start

task_list = []


def handle_exit(arg1, arg2):
    print("Получен сигнал SIGINT (Ctrl+C). Завершение программы...")
    # tasks = asyncio.all_tasks()
    for task in task_list:
        print("Отмена задачи:", task.get_name() or task)
        task.cancel()


async def main():
    global task_list
    tasks = [
        create_socket(),
        discord_bot_start(),
        telegram_bot_start()
    ]

    # Оборачиваем каждую корутину в объект asyncio->Task
    task_list = [asyncio.create_task(task) for task in tasks]

    try:
        # Планируем задачи
        await asyncio.gather(*task_list)
    except asyncio.CancelledError:
        print("Прервано пользователем")


if __name__ == "__main__":
    # Вешаем обработчик выхода из программы
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    # Запускаем асинхронные задачи и ждём выполнения
    task_list = asyncio.run(main())
