FROM python:3.10

WORKDIR /tasty_delivery

COPY poetry.lock pyproject.toml .

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install -n --no-root --no-dev

COPY tasty_delivery .
ENV PYTHONPATH "/tasty_delivery"
# ENV DB_HOST "postgres_db"

ENTRYPOINT uvicorn server:app --host 0.0.0.0 --port 8000