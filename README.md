# anyon

[![Maintainability](https://api.codeclimate.com/v1/badges/aec281977aceffb74d10/maintainability)](https://codeclimate.com/github/nepstock/anyon/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/aec281977aceffb74d10/test_coverage)](https://codeclimate.com/github/nepstock/anyon/test_coverage)

## Run

```bash
pipenv run gunicorn --reload 'src.app:get_app()'
```

## Tests

```bash
pipenv run pytest -p no:cacheprovider --cov-report term-missing --cov=src -s
```

## Docker compose

```bash
docker-compose -f deploy/docker-compose.yml up
```
