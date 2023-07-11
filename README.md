<div>
  <img src="static/img/atena.png" alt="Atena Saotome" width="100" />
</div>

# Atena

A place for dropping a build artifact from CI pipelines

This project design for self-hosted to store build artifact from CI pipelines more properly and can control the artifact access more than GitHub Action give.

## Start developing atena

This project required

- [Python 3.11](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)

Copy `.env.example` to `.env` and fill the value

```bash
cat .env.example > .env
```

Install dependencies

```bash
poetry install
```

Migrate database

```bash
poetry run python manage.py migrate
```

Run server

```bash
poetry run python manage.py runserver
```

If you want to stay in the poetry shell, you can run

```bash
poetry shell
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details