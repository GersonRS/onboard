PROJECT_SERVE=service_api_classifier
PROJECT_GRPC=processing
TIME=60

# colors
GREEN = $(shell tput -Txterm setaf 2)
YELLOW = $(shell tput -Txterm setaf 3)
WHITE = $(shell tput -Txterm setaf 7)
RESET = $(shell tput -Txterm sgr0)
GRAY = $(shell tput -Txterm setaf 6)
TARGET_MAX_CHAR_NUM = 20

# Common

all: run

## Runs application. Builds, creates, starts, and attaches to containers for a service. | Common
run:
	@docker-compose up $(PROJECT_SERVE)

## Rebuild service_api_classifier container
build:
	@docker-compose build $(PROJECT_SERVE)

## Stops application. Stops running container without removing them.
stop:
	@docker-compose stop

## Removes stopped service containers.
clean:
	@docker-compose down

docker-clean:
	@docker system prune -f

## Runs command `bash` commands in docker container.
bash:
	@docker exec -it $(PROJECT_SERVE) bash

## Upgrade your python's dependencies:
upgrade:
	docker-compose run --rm $(PROJECT_SERVE) python3 -m $(PROJECT_SERVE).utils.check-requirements

## Create profile sampling of application.
profile:
	@docker exec -it $(PROJECT_SERVE) py-spy record -d $(TIME) -o $(PROJECT_SERVE)_profile.svg --pid 9

# Help

## Shows help.
help:
	@echo ''
	@echo 'Usage:'
	@echo ''
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
		    if (index(lastLine, "|") != 0) { \
				stage = substr(lastLine, index(lastLine, "|") + 1); \
				printf "\n ${GRAY}%s: \n\n", stage;  \
			} \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			if (index(lastLine, "|") != 0) { \
				helpMessage = substr(helpMessage, 0, index(helpMessage, "|")-1); \
			} \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
	@echo ''

# Linters & tests

## Formats code with `black`. | Linters
black:
	@docker-compose run --rm $(PROJECT_SERVE) black $(PROJECT_SERVE) --exclude $(PROJECT_SERVE)/migrations -l 79

## Checks types with `mypy`.
mypy:
	@docker-compose run --rm $(PROJECT_SERVE) mypy $(PROJECT_SERVE)

## Formats code with `flake8`.
lint:
	@docker-compose run --rm $(PROJECT_SERVE) flake8 $(PROJECT_SERVE)

## Runs tests. | Tests
test: lint
	@docker-compose up test
	@docker-compose stop test

## Runs application with development config.
adev:
	adev runserver ./$(PROJECT_SERVE)/__main__.py -p 8080

## Runs application with specified postgres and redis.
wait_resources:
	python3 -m $(PROJECT_SERVE).utils.wait_script
