import subprocess
import sys
import os
import webbrowser
import time


def get_base_path():
    """Возвращает правильный путь для exe и для скрипта"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


def run_command(cmd, cwd=None):
    """Выполняет команду и возвращает успешность"""
    try:
        if cwd is None:
            cwd = get_base_path()
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        print(f"Ошибка выполнения команды: {e}")
        return False, "", str(e)


def check_and_install_dependencies():
    """Проверяет и устанавливает зависимости"""
    print("\n" + "=" * 60)
    print("ПРОВЕРКА ЗАВИСИМОСТЕЙ")
    print("=" * 60)

    dependencies = [
        ('django', 'Django'),
        ('PIL', 'Pillow'),
    ]

    all_ok = True
    for package, install_name in dependencies:
        print(f"Проверка {package}...", end=' ')
        success, _, _ = run_command(f'python -c "import {package}"')
        if success:
            print("✓ OK")
        else:
            print("✗ НЕ НАЙДЕН")
            print(f"  Установка {install_name}...", end=' ')
            success, _, _ = run_command(f'python -m pip install {install_name}')
            if success:
                print("✓ Успешно")
            else:
                print("✗ Ошибка")
                all_ok = False
    return all_ok


def check_migrations():
    """Проверяет наличие миграций"""
    print("\n" + "=" * 60)
    print("ПРОВЕРКА МИГРАЦИЙ")
    print("=" * 60)

    success, stdout, stderr = run_command('python manage.py showmigrations')

    if "No migrations" in stdout or not stdout.strip():
        print("Миграции не найдены. Создаем и применяем...")
        success, stdout, stderr = run_command('python manage.py makemigrations')
        if success:
            print("✓ Миграции созданы")
            success, stdout, stderr = run_command('python manage.py migrate')
            if success:
                print("✓ Миграции применены")
                return True
            else:
                print(f"✗ Ошибка применения миграций: {stderr}")
                return False
        else:
            print(f"✗ Ошибка создания миграций: {stderr}")
            return False
    elif "[ ]" in stdout or "не применены" in stdout:
        print("Обнаружены непримененные миграции. Применяем...")
        success, stdout, stderr = run_command('python manage.py migrate')
        if success:
            print("✓ Миграции успешно применены")
            return True
        else:
            print(f"✗ Ошибка применения миграций: {stderr}")
            return False
    else:
        print("✓ Миграции в порядке")
        return True


def create_superuser():
    """Создает суперпользователя, если его нет"""
    print("\n" + "=" * 60)
    print("ПРОВЕРКА СУПЕРПОЛЬЗОВАТЕЛЯ")
    print("=" * 60)

    success, stdout, stderr = run_command(
        'python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())"')

    if "False" in stdout:
        print("Суперпользователь не найден")
        print("Создаем суперпользователя...")

        username = input("Логин (по умолчанию admin): ").strip()
        if not username:
            username = "admin"

        email = input("Email (по умолчанию admin@healthfood.ru): ").strip()
        if not email:
            email = "admin@healthfood.ru"

        password = input("Пароль (по умолчанию admin123): ").strip()
        if not password:
            password = "admin123"

        create_cmd = f'python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser(\'{username}\', \'{email}\', \'{password}\')"'
        success, stdout, stderr = run_command(create_cmd)

        if success:
            print(f"✓ Суперпользователь '{username}' создан")
            return True
        else:
            print(f"✗ Ошибка создания суперпользователя: {stderr}")
            return False
    else:
        print("✓ Суперпользователь уже существует")
        return True


def run_server():
    """Запускает сервер Django"""
    print("\n" + "=" * 60)
    print("ЗАПУСК СЕРВЕРА")
    print("=" * 60)

    print("Запуск Django сервера...")
    print("Сайт будет доступен по адресу: http://127.0.0.1:8000")
    print("Админ-панель: http://127.0.0.1:8000/admin")
    print("\nДля остановки сервера нажмите Ctrl+C в этом окне")
    print("=" * 60)

    def open_browser():
        time.sleep(2)
        webbrowser.open('http://127.0.0.1:8000')

    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    try:
        subprocess.run(['python', 'manage.py', 'runserver'], cwd=get_base_path(), check=True)
    except subprocess.CalledProcessError as e:
        print(f"Сервер завершился с ошибкой: {e}")
    except KeyboardInterrupt:
        print("\n\nСервер остановлен пользователем")

    input("\nНажмите Enter для выхода...")


def main():
    """Главная функция"""
    print("\n" + "=" * 60)
    print("   HEALTHY FOOD RECIPES - КАТАЛОГ РЕЦЕПТОВ")
    print("   Калькулятор калорий и шопинг-лист")
    print("=" * 60)

    base_path = get_base_path()
    os.chdir(base_path)

    if not os.path.exists("manage.py"):
        print("ОШИБКА: Файл manage.py не найден!")
        print(f"Ищем в: {base_path}")
        print("\nУбедитесь, что лаунчер находится в папке с проектом")
        input("\nНажмите Enter для выхода...")
        return

    print("\nПроверка Python...")
    success, stdout, stderr = run_command('python --version')
    if not success:
        print("✗ ОШИБКА: Python не найден!")
        print("Установите Python 3.10 или выше и добавьте его в PATH")
        input("\nНажмите Enter для выхода...")
        return
    print(f"✓ {stdout.strip()}")

    if not check_and_install_dependencies():
        print("\n✗ ОШИБКА: Не удалось установить все зависимости")
        input("\nНажмите Enter для выхода...")
        return

    if not check_migrations():
        print("\n✗ ОШИБКА: Проблемы с миграциями")
        print("Попробуйте выполнить вручную: python manage.py migrate")
        input("\nНажмите Enter для выхода...")
        return

    if not create_superuser():
        print("\n✗ ОШИБКА: Не удалось создать суперпользователя")
        input("\nНажмите Enter для выхода...")
        return

    run_server()


if __name__ == "__main__":
    main()