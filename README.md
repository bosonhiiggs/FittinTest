# Меха и шубы
Этот проект представляет собой backend для интернет-магазина "Меха и шубы", реализованный на Django.

## Требования

- Python 3+
- PostgreSQL 13+
- Docker

## Установка и настройка проекта

### 1. Клонирование проекта
```bash
git clone https://github.com/
cd
```

### 2. Активация виртуального окружения
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей
```bash
pip install poetry
poetry install
```

### 4. Настройка базы данных
Для начала необходимо перейти в терминал сервера DB, затем настроить все необходимые разрешения
```bash
sudo -u postgres psql
CREATE DATABASE myshopfittin;
CREATE USER myshop_user WITH PASSWORD 'fittin-test';
ALTER ROLE user SET client_encoding 'utf8';
ALTER ROLE user SET timezone 'UTC';
GRANT ALL PRIVILEGES ON DATABASE myshop_db TO myshop_user;
\q
```

### 5. Настройка переменных окружения
Вы можете использовать переменные из файла .env, а можете использовать шаблон для своих настроек .env.template

### 6. Сборка docker
Для доступа к проекту не из Docker, необходимо указать в settings.py `HOST: 'localhost'`(Это указано в комментариях).
```bash
docker compose build
```

### 7. Запуск проекта
```bash
docker compose up
```

### 8. Применение миграций
```bash
docker compose exec -it app bash
python manage.py migrate
exit
```
### 9.* Загрузка фикстур
Фикстура сразу имеет учетную запись для доступа к Admin-панели (username: admin, password: 123)
```bash
docker compose exec -it app bash
python manage.py loaddata dbdump.json
exit
```

Для доступа к проекту необходимо перейти по адресу: http://0.0.0.0:8000/

Для доступа к документации необходимо перейти по адресу: http://0.0.0.0:8000/api/docs/

