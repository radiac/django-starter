# {{ cookiecutter.project_name }}

## Development

Run using docker compose:

```bash
# Run the postgres and django containers
docker compose up postgres
docker compose up django
# Connect to the running django container
docker compose exec django /bin/bash
# Start the Django container without running Django
docker compose run --service-ports --entrypoint=/bin/bash django
```

The database container has a script to dump from the database:

```bash
docker compose exec postgres /project/docker/postgres/dump.sh
```

The dumped file is in `../docker-store/backup`

To load the database from a dump (default `database.dump`):

```bash
docker compose exec postgres /project/docker/postgres/restore.sh
```

Testing
-------

The project is configured to use `pytest`:

```bash
pytest
```


Deployment
==========

* Run ``manage.py compress` to compress assets before `manage.py collectstatic`
