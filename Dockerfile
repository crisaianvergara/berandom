FROM python:3.11-slim

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

WORKDIR /code

COPY poetry.lock pyproject.toml README.md ./
RUN poetry install --no-root
COPY . .

CMD ["python", "main.py"]