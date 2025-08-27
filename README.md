# Django starter project

This is the template project I use for most of my Django projects. It is a simple set of
extras applied to Django's core, designed for building conventional server-side rendered
multi-page apps.

Developer experience:

* `pre-commit` hook with ruff
* `docker compose` config for local development
* `uv` for managing dependencies
* `pytest` support
* support for multi-line template tags

Production features:

* ``compressor`` and ``whitenoise`` for managing static files


## Quickstart: Standard

The recommended way to create your project is using
[uv](https://github.com/astral-sh/uv) and
[cookiecutter](https://www.cookiecutter.io/):

```bash
pip install uv pre-commit
uvx cookiecutter@latest gh:radiac/django-starter --directory cookiecutter
```

You'll be asked three questions:

* Project name: the human-readable site title
* Project slug: the app name for the site
* Root dir: this will appear in your current dir as your git project root

This will

* create a directory for your root dir and apply the cookiecutter inside it
* inside that, create a virtualenv in `.venv` and install dependencies using
  [uv](https://github.com/astral-sh/uv)
* create a git repository in the root dir and make an initial commit
* install pre-commit hooks using [pre-commit](https://pre-commit.com/)

You can then use [docker compose](https://docs.docker.com/compose/) for local
development:

```bash
# Run the postgres and django containers
docker compose up postgres
docker compose up django
# Connect to the running django container
docker compose exec django /bin/bash
# Start the Django container without running Django
docker compose run --service-ports --entrypoint=/bin/bash django
```

This project supports [workenv](https://github.com/radiac/workenv); run
`workenv --add myproject` from your project root; you can then:

```bash
we myproject postgres
we myproject django
we myproject django-shell
```


## Quickstart: Nanodjango

To use this cookiecutter with `nanodjango convert`
([see docs](https://nanodjango.readthedocs.io/en/latest/convert.html)):

```bash
mkdir template
cd template
pip install uv pre-commit
uvx cookiecutter@latest gh:radiac/django-starter --directory cookiecutter
```

Answer with the following values:

* `project_name`: `{{ project_name }}`
* `project_slug`: `{{ project_name }}`
* `root_dir`: `{{ project_directory }}`

Now use it as the template for nanodjango:

```bash
cd ..
nanodjango convert <script.py> new_project_dir --name=<project_name> --template=template/<project_name> --delete
```

You can now delete the `template` directory.

See Standard quickstart for notes on using this new project.


## Quickstart: Manual

If you don't want to use cookiecutter or docker compose, you can do everything manually.

Check out the project:

```bash
git clone https://github.com/radiac/django-starter.git /tmp/starter
mv /tmp/starter/src /path/to/myproject
rm -r /tmp/starter
```

Set up a Python virtual environment and install project dependencies

```bash
pip install uv
cd /path/to/myproject
uv venv .venv
source .venv/bin/activate
uv pip compile requirements.in -o requirements.txt
uv pip sync requirements.txt
cp compose.dev.yaml compose.yaml
git init
uvx pre-commit@latest install
```

Go through the code you copied and replace `starter` with the name of your project.

You can then run the Django project as normal:

```bash
# run local postgres or update settings
./manage.py migrate
./manage.py runserver 0:8000
```


## Using the database

The database container has a script to dump from the database:

```bash
docker compose exec postgres /project/docker/postgres/dump.sh
```

The dumped file is in `../docker-store/backup`

To load the database from a dump (default `database.dump`):

```bash
docker compose exec postgres /project/docker/postgres/restore.sh
```


## Testing

The project is configured to use `pytest`:

```bash
pytest
```


## Deployment

There is a `compose.live.jinja2` and `d0s-manifest.yaml` for docker0s deployment. It
expects a standard docker0s Traefik installation with an open internal mail relay.

Alternatively this project can be deployed using any standard method, but note:

* Run ``manage.py compress` to compress assets before `manage.py collectstatic`


## Contributing

Fork from the latest Django version branch and make changes in `src/`.

To test your src project in place using sqlite, run it with:

```bash
cd src
./manage.py runserver --configuration=Local
```

To build a new cookiecutter:

```bash
python build.py --delete
```

Test the cookiecutter locally using:

```bash
cd /tmp
uvx cookiecutter path/to/django-starter/cookiecutter
```

### Branches

Each `django-V.v` branch has the latest customisations for that version of Django -
older versions are not updated. Each branch starts from a commit tagged
`base-django-V.v` and replays customisations. The current version of Django is the main
branch in the repository.

To make changes to the current project, edit `django-V.v`, using the most recent Django
version implemented by this project.


## Credits

* ``robots.txt`` from `Neil Clarke
  <https://neil-clarke.com/block-the-bots-that-feed-ai-models-by-scraping-your-website/>`_
