FROM httpd:2.4.65

RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

COPY htdocs /usr/local/apache2/htdocs

EXPOSE 80
