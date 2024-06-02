include .env

.PHONY: core-build api-build devcontainer-build


core-build:
	[ -e .secrets/.env ] || touch .secrets/.env
	docker compose build inkywhat-dsp-core

core-run:
	docker compose run inkywhat-dsp-core


devcontainer-build: core-build
	docker compose -f .devcontainer/docker-compose.yml build inkywhat-dsp-devcontainer

devcontainer-run: devcontainer-build
	docker compose -f .devcontainer/docker-compose.yml run inkywhat-dsp-devcontainer


api-build: core-build
	docker compose build inkywhat-dsp-api

api-run: api-build
	docker compose run inkywhat-dsp-api

api-up: api-build
	docker compose up inkywhat-dsp-api -d
