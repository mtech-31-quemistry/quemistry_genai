FROM python:3.12-slim

RUN pip install poetry

COPY . .

RUN poetry install

EXPOSE 80

ENTRYPOINT ["poetry", "run", "python", "-m", "question.server"]
