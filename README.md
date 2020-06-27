# anyon

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
