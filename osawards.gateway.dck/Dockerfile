FROM python:3.12-slim-bookworm

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

# Install other packages
RUN apt-get update \
    && apt install curl iputils-ping -y \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 5010

ENTRYPOINT ["sh", "./init.sh"]
