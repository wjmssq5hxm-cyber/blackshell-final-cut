# Railway

Private Django site. The `Procfile` is the source of truth:

```
web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

If the Railway UI has a **Start Command** set, it overrides the Procfile `web` line — it must match the `web:` line above. Leave **Custom Start Command** empty to use the Procfile.

## Required variables

| Variable | Value |
|---|---|
| `DJANGO_SECRET_KEY` | 50+ random characters (not the local `change-me`) |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_ALLOWED_HOSTS` | `<app>.up.railway.app` (add `blackshell.tech,www.blackshell.tech` later) |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://<app>.up.railway.app` |
| `DJANGO_SECURE_SSL_REDIRECT` | `False` until that URL is healthy, then `True` |
| `DATABASE_URL` | set automatically if you attach Railway Postgres |

Optional: `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`, `CONTACT_TO_EMAIL`, `EDITOR_PASSWORD`.

After the first healthy deploy, run `python manage.py seed_site` from a one-off shell (needs `EDITOR_PASSWORD` when `DEBUG` is off), then change the editor password.

`GET /healthz` returns `ok` and is a good health-check path.
