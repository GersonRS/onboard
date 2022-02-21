# service_api_classifier

___

## Requirements
- docker-compose

___

## Features

- aiohttp
- mypy
- pytest
- flake8
- trafaret
- docker-compose
- aio devtools
- black
- aiohttp debug toolbar


## Local development
All the development settings are stored in `/config/api.dev.yml`.

### Run
To start the project in development mode, run the following command:

```
make run
```

or just

```
make
```

To stop docker containers:

```
make stop
```

To clean up docker containers (removes containers, networks, volumes, and images created by docker-compose up):

```
make clean
```

Shell inside the running container

```
make bash # the command can be executed only if the server is running e.g. after `make run`
```


### Upgrade
To upgrade dependencies:

```
make upgrade
```

### Help

List available `Makefile` commands
```
make help
```

### Docs

To generate sphinx docs
```
make doc
```

### Linters
To run flake8:

```
make lint
```

All the settings for `flake8` can be customized in `.flake8` file

### Type checking
Run mypy for type checking:

```
make mypy
```

Settings for `mypy` can be customized in the `mypy.ini` file.

___

## Software

- python3.7
