# Black Shell Technology — final cut

Chicago-regional marketing site. Frost-steel theme. Every word and photo is
editable at **`/editor/`** — no code required.

## Run it locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

npm install
npm run build:css

copy .env.example .env
python manage.py migrate
python manage.py seed_site
python manage.py runserver
```

- Site: http://127.0.0.1:8000
- Editor: http://127.0.0.1:8000/editor/
- Login: `editor` / `blackshell`  (change this before anything faces the internet:
  `python manage.py changepassword editor`)

When editing styles, run `npm run watch:css` in a second terminal.

## Cloudflare quick tunnel (local demo)

With `DJANGO_DEBUG=True`, Django accepts any Host header so a Cloudflare
quick tunnel works without listing a hostname. Restart **runserver** after
changing this setting — `ALLOWED_HOSTS` is read at process start.

```bash
python manage.py runserver
cloudflared tunnel --url http://127.0.0.1:8000
```

Restarting `cloudflared` mints a **new** `*.trycloudflare.com` host. You do
not need to edit settings for that; just use the URL it prints.

When `DJANGO_DEBUG` is off, only the hosts in `DJANGO_ALLOWED_HOSTS` (and
origins in `DJANGO_CSRF_TRUSTED_ORIGINS`) are allowed.

## What the owner edits

| In the editor | What it changes |
|---|---|
| **Site text** | Headlines, phone, email, about copy, every page of writing |
| **Home page cards** | Design / Build / Service — including photos |
| **Services / Tech services** | The three big services and the long tech list |
| **Projects** | Portfolio items with a cover photo and an optional gallery |
| **Journal posts** | Optional news. Stay hidden until “Show on the website” is checked |
| **Job openings** | Careers list |
| **Marquee lines** | The ticker in the footer |
| **Contact form inquiries** | Messages visitors sent |

One bullet per line in the bullet-list boxes. Leave a photo empty and a placeholder is used.

## Tests

```bash
python manage.py test
python manage.py check --deploy
```

## Go live

Do this on the machine that will serve the public site. Do **not** copy the local `.env` as-is.

1. **Generate a real secret and turn DEBUG off**

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

   In `.env`:

   ```
   DJANGO_DEBUG=False
   DJANGO_SECRET_KEY=<the value you just generated>
   DJANGO_ALLOWED_HOSTS=blackshell.tech,www.blackshell.tech
   DJANGO_CSRF_TRUSTED_ORIGINS=https://blackshell.tech,https://www.blackshell.tech
   ```

2. **Change the editor password** — `python manage.py changepassword editor`

3. **Replace starter copy** in `/editor/` → Site text: phone, license number, email. The seed data uses a 555 number on purpose.

4. **Send contact-form mail for real** — set `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, and a `DEFAULT_FROM_EMAIL` on a domain you control (not `onboarding@resend.dev`). Inquiries are always saved in `/editor/` even if mail fails.

5. **Build assets and collect static files**

   ```bash
   npm run build:css
   python manage.py collectstatic --noinput
   python manage.py migrate
   python manage.py check --deploy
   ```

6. **Run gunicorn** behind HTTPS (Cloudflare, nginx, or a host that terminates TLS):

   ```bash
   gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2
   ```

   After HTTPS is confirmed working, set `DJANGO_HSTS_SECONDS=31536000` and restart. Do not enable HSTS while you are still testing HTTP.

Health check: `GET /healthz` returns `ok`. Uploaded photos live in `media/` and are served by the app on a single-server deploy.
