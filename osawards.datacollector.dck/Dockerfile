FROM python:3.10-alpine

# Install poetry and disable virtualenvs inside docker
RUN pip install poetry  \
    && poetry config virtualenvs.create false

# Copy dependency files first
WORKDIR /app
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the app
COPY . /app

# Adjust permissions
RUN chmod 777 /app/data && \
    chmod 777 /app/templates

CMD sh ./init.sh
