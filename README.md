# Django AI Job Assistant (Web App)

The main **Django web application** for an AI-powered job-application assistant:
a chat-driven UI that helps users build resumes and generate tailored cover
letters, with a dashboard, cover-letter tracking, and user accounts. Built on
[cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django).

This is de-branded reference / portfolio code from a production app. Real
secrets, hosts, and a scraped third-party data file have been removed; external
integration points are now environment variables or `YOUR_*` placeholders.

## Apps (`jobassistant/`)

| App | Purpose |
|-----|---------|
| `chat` | Chat interface to the assistant (talks to a Rasa backend) |
| `resume` | Resume builder + position/industry data |
| `cover_letter` | Cover-letter creation |
| `cover_letter_tracking` | Track sent cover letters / applications |
| `dashboard` | User dashboard + document templates |
| `users` | Accounts (django-allauth) |
| `contact` | Contact form |
| `taskapp` | Celery task app |

## Stack

Django · cookiecutter-django · Celery · Redis · Postgres · S3 (storages) ·
WeasyPrint (PDF) · Rasa (external chat backend)

## Setup

```bash
pip install -r requirements/local.txt   # see requirements/
cp .env.example .env                     # fill in values

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Run a Celery worker (from the dir with `manage.py`):

```bash
celery -A jobassistant.taskapp worker -l info
```

## Configuration

Settings live in `config/settings/` (`base.py`, `local.py`, `production.py`,
`staging.py`). All secrets are read from the environment — see `.env.example`,
`SECRET_KEY` (`DJANGO_SECRET_KEY`), database (`DB_PASSWORD`, RDS host vars), S3
buckets, and the Rasa core URL. Never commit real credentials.

> Note: collected `staticfiles/`, AWS `.ebextensions`/Elastic Beanstalk config,
> Terraform, CodeBuild buildspecs, and a scraped company-data file from the
> original repo were intentionally excluded.

## License

MIT — see [LICENSE](LICENSE).
