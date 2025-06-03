# DocuHub

## Описание
DocuHub — это платформа для публикации и просмотра документации. Пользователи могут регистрироваться, создавать и редактировать свои посты, а администратор может удалять пользователей и документы через админ-панель.

## Структура проекта
```
FlaskProject_modified/
├── app/
│   ├── __init__.py
│   ├── forms.py
│   ├── models.py
│   ├── routes.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   └── templates/
│       ├── admin_panel.html
│       ├── base.html
│       ├── dashboard.html
│       ├── doc_edit.html
│       ├── doc_view.html
│       ├── edit_profile.html
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       └── user_profile.html
├── instance/
│   └── config.py
├── migrations/
├── Procfile
├── README.md
├── requirements.txt
├── runtime.txt
└── run.py
```

## Установка и запуск локально
1. Клонируйте репозиторий или распакуйте архив.
2. Перейдите в корневую папку проекта:
   ```bash
   cd FlaskProject_modified
   ```
3. Создайте виртуальное окружение и активируйте его:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # для Linux/Mac
   venv\Scripts\activate   # для Windows
   ```
4. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
5. (Опционально) Отредактируйте `instance/config.py`, чтобы изменить `SECRET_KEY` и `SQLALCHEMY_DATABASE_URI` (пример для PostgreSQL):
   ```python
   SECRET_KEY = 'your-production-secret-key'
   SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@hostname:port/dbname'
   ```
6. Инициализируйте базу данных:
   ```bash
   flask db upgrade  # если используете Flask-Migrate
   # Или просто:
   python run.py
   ```
7. Запустите приложение:
   ```bash
   python run.py
   ```
8. Откройте браузер и перейдите по адресу `http://127.0.0.1:5000`.

## Деплой на Heroku
1. Зарегистрируйтесь или войдите в Heroku.
2. Установите Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
3. Войдите через CLI:
   ```bash
   heroku login
   ```
4. Создайте новое приложение:
   ```bash
   heroku create your-app-name
   ```
5. Добавьте PostgreSQL аддон:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```
6. Установите удаленный репозиторий (если еще не установлен):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   heroku git:remote -a your-app-name
   ```
7. Задайте переменные окружения:
   ```bash
   heroku config:set SECRET_KEY='your-production-secret-key'
   ```
   Heroku автоматически устанавливает `DATABASE_URL` для PostgreSQL. Убедитесь, что в `instance/config.py` или основном приложении используется `os.environ.get('DATABASE_URL')` для `SQLALCHEMY_DATABASE_URI`.
8. Добавьте Procfile (уже включен) и requirements.txt (уже должен быть сгенерирован).
9. Запушьте изменения:
   ```bash
   git push heroku main
   ```
10. Выполните миграции (если используются):
    ```bash
    heroku run flask db upgrade
    ```
11. Откройте приложение:
    ```bash
    heroku open
    ```

## Деплой на другой хостинг (PythonAnywhere, DigitalOcean и т.д.)
1. Создайте виртуальный сервер/аккаунт.
2. Скопируйте файлы проекта.
3. Создайте виртуальное окружение, установите зависимости.
4. Настройте веб-сервер (Gunicorn + Nginx) или используйте встроенный WSGI (например, для PythonAnywhere).
5. Укажите переменные окружения для `SECRET_KEY` и `SQLALCHEMY_DATABASE_URI`.
6. Инициализируйте и мигрируйте базу данных.
7. Перезапустите сервис.

---
