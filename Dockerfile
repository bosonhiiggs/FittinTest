FROM python:3.10-slim

ENV PUTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip poetry
RUN poetry config virtualenvs.create false --local
COPY poetry.lock pyproject.toml ./
RUN poetry install

RUN poetry show

COPY myshop .
RUN python manage.py collectstatic --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
