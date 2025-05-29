# Simple nats-jestream app

Simple app to demonstrate use of docker, uv and nat-jetstream

## Dependencies
[UV](https://docs.astral.sh/uv/)
[Python](https://www.python.org/)
[Docker](https://www.docker.com/)

### Install UV

[Install uv docs](https://docs.astral.sh/uv/getting-started/installation/#pypi)

`curl -LsSf https://astral.sh/uv/install.sh | sh`

or

`brew install uv`

### Install Python
`uv python install`

## Make commands
`make help`
``
>Makefile commands:
>  clean       - Remove virtual environment and pycache
>  clean-build - Build new docker images
>  relock      - Build new uv.lock file
>  run         - Run project in docker
>  setup       - Setup venv, install python deps from pyproject.toml
>  test        - Run pytest tests
>  test-int    - Run pytest integration tests
``
