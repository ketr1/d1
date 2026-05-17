Установка и запуск:

1. Установите зависимости:
pip install -r requirements.txt

2. Выполните миграции:
python manage.py makemigrations
python manage.py migrate

3. Создайте суперпользователя:
python manage.py createsuperuser

4. Запустите сервер:
python manage.py runserver

5. Откройте в браузере:
http://127.0.0.1:8000/