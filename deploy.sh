#!/bin/bash

sudo docker compose \
	--env-file .env-sftp \
	--env-file .env-elasticsearch \
	--env-file .env-kibiter \
	--env-file .env-gateway \
	--env-file .env-datacollector \
	--env-file .env-framework \
	--env-file .env-portainer \
	--env-file .env-traefik \
	up -d
