# Cipher Lab — Django Project

A Django web app implementing three classical/modern cryptography techniques,
built for a cryptography assignment:

1. **Rail Fence Cipher** — encrypt/decrypt via `ciphers/logic/rail_fence.py`
2. **RSA Encryption** — keypair generation, encrypt/decrypt via `ciphers/logic/rsa_cipher.py`
3. **MD5 / SHA-256 password hashing** — used for account registration and login
   via `accounts/hashing.py`

All three are implemented from scratch using only Python's standard library
(`hashlib`, `random`) — no third-party crypto packages.

## How the login/hashing requirement is satisfied

- Registration (`/accounts/register/`) lets you pick **MD5** or **SHA-256**.
  The chosen algorithm hashes the password immediately; only the resulting
  hash (and the algorithm name) is saved to the `CustomUser` model in the
  database — the plaintext password is never stored.
- Login (`/accounts/login/`) re-hashes the submitted password with the same
  algorithm used at registration and compares it to the stored hash. Access
  is only granted on an exact match.
- You can see the stored hash directly in the Django admin
  (`/admin/`, register a superuser first — see below) or right after
  registering, where the success message shows the exact hash that was saved.

This intentionally bypasses Django's own built-in password hasher (PBKDF2)
so the MD5/SHA-256 hash is visible and inspectable, per the assignment's
requirement. `accounts/hashing.py` has a short note on why MD5/unsalted
SHA-256 wouldn't be used this way in a real production system.

## Project structure

```
cipher_project/        Django project settings/urls
accounts/               Custom user model, registration/login/logout, hashing.py
ciphers/                 Dashboard + tool views
  logic/
    rail_fence.py        Rail Fence cipher implementation
    rsa_cipher.py         RSA implementation (prime gen, keygen, encrypt, decrypt)
templates/                All HTML templates
static/css/style.css      Custom styling (no framework/CDN dependency besides Google Fonts)
```

## Running locally

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

Visit `http://127.0.0.1:8000/accounts/register/` to create an account, then
log in and use the Rail Fence / RSA tools from the dashboard.

## Deploying for free (submission link)

**Recommended: PythonAnywhere** (free tier, no credit card, Django-native)

1. Create a free account at pythonanywhere.com.
2. Open a Bash console and upload/clone this project (or use the Files tab
   to upload the zip and unzip it).
3. Create a virtualenv and install requirements:
   ```bash
   mkvirtualenv --python=python3.10 cipherlab
   pip install -r requirements.txt
   ```
4. Go to the **Web** tab → **Add a new web app** → **Manual configuration**
   → pick your Python version.
5. Set the **virtualenv** path to the one you created.
6. Edit the WSGI file it generates to point to `cipher_project.wsgi.application`
   (uncomment/edit the Django section, set the project path and settings module).
7. In the **Static files** section, map URL `/static/` to your project's
   `staticfiles/` folder (run `python manage.py collectstatic` first).
8. Reload the web app. Your submission link is the `*.pythonanywhere.com`
   URL shown at the top of the Web tab.

**Alternative: Render**
1. Push this project to a GitHub repo.
2. Create a new **Web Service** on render.com, connect the repo.
3. Build command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
4. Start command: `gunicorn cipher_project.wsgi`
5. Add environment variable `DJANGO_ALLOWED_HOSTS` = `*` (or your `.onrender.com` domain).
6. Note: the free tier spins down after inactivity, so the first load after
   idling takes ~30 seconds — normal for a free demo link.

Either way, before submitting, set `DJANGO_DEBUG=False` as an environment
variable on the host so Django doesn't run in debug mode in production.

## Notes on the RSA implementation

For a fast, readable classroom demo, keys are generated from 16-bit random
primes (not the 1024+ bit primes real-world RSA uses), so key generation is
instant in the browser. The math (Miller-Rabin primality test, modular
exponentiation, the Extended Euclidean Algorithm for the modular inverse) is
the same math full-size RSA uses — only the key size is scaled down.
