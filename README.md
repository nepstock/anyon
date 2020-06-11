# anyon

## Run

```bash
pipenv run gunicorn --reload 'src.app:get_app()'
```

## Tests

```bash
pipenv run pytest -s
```

## Docker compose

```bash
docker-compose -f deploy/docker-compose.yml up
```
