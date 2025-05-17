.PHONY: core-build api-build devcontainer-build


core-build:
	docker compose build inky-dsp-core

core-run:
	docker compose run inky-dsp-core


devcontainer-build: core-build
	docker compose -f .devcontainer/docker-compose.yml build inky-dsp-devcontainer


api-build: core-build
	docker compose build inky-dsp-api

api-run: api-build
	docker compose run --rm inky-dsp-api

api-up: api-build
	docker compose up inky-dsp-api -d

api-stop:
	docker compose stop inky-dsp-api
