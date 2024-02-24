"""
    Скрипт для разворачивания виртуального окружения и установки зависимостей
"""

import subprocess
import sys

ENV_NAME = 'project-env'

errors_count = 0


def increase_errors_count():
    global errors_count
    errors_count += 1


def install_pip():
    try:
        subprocess.check_call([sys.executable, '-m', 'ensurepip', '--upgrade'])
        print("\033[32m", "pip успешно установлен.", "\033[0m")
    except subprocess.CalledProcessError as e:
        increase_errors_count()
        print("\033[31m", "При установке pip произошла ошибка:", e, "\033[0m")


def install_virtualenv():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'virtualenv'])
        print("\033[32m", "virtualenv успешно установлен.", "\033[0m")
    except subprocess.CalledProcessError as e:
        increase_errors_count()
        print("\033[31m", "При установке virtualenv произошла ошибка:", e, "\033[0m")


def create_virtualenv():
    try:
        subprocess.check_call([sys.executable, '-m', 'virtualenv', ENV_NAME])
        print("\033[32m", "Виртуальная среда создана успешно.", "\033[0m")
    except subprocess.CalledProcessError as e:
        increase_errors_count()
        print("\033[31m", "Произошла ошибка при создании виртуальной среды:", e, "\033[0m")


def activate_virtualenv():
    if sys.platform == 'win32':
        activate_cmd = 'myproject_env\\Scripts\\activate'
    else:
        activate_cmd = f'source {ENV_NAME}/bin/activate'

    try:
        subprocess.check_call(activate_cmd, shell=True)
        print("\033[32m", "Виртуальная среда успешно активирована.", "\033[0m")
    except subprocess.CalledProcessError as e:
        increase_errors_count()
        print("\033[31m", "Произошла ошибка при активации виртуальной среды:", e, "\033[0m")


def install_dependencies():
    try:
        subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
        print("\033[32m", "Зависимости успешно установлены.", "\033[0m")
    except subprocess.CalledProcessError as e:
        increase_errors_count()
        print("\033[31m", "Произошла ошибка при установке зависимостей:", e, "\033[0m")


if __name__ == "__main__":
    install_pip()
    install_virtualenv()
    create_virtualenv()
    activate_virtualenv()
    install_dependencies()
    if errors_count > 0:
        print("\033[1m" + "\033[31m", "Во время выполнения скрипта возникли ошибки.")
    print("\033[0m")
