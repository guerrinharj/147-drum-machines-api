# 147 Drum Machines API (Django + Supabase)

Backend API for **147 Drum Machines**.
- Django + Django REST Framework
- Supabase Postgres (DB)
- Supabase Storage (audio + images via signed URLs)

---

## Requirements

- macOS + zsh
- Homebrew
- Python 3 (via Homebrew)

Install Python (one-time):
```zsh
brew install python
```



### Project Setup (one-time)

From the project root (where manage.py is):

#### 1. Create and activate virtual environment
```zsh
python3 -m venv .venv
source .venv/bin/activate
```

#### 2. Install dependencies

Note: zsh needs quotes for psycopg[binary].

```zsh
python -m pip install --upgrade pip
python -m pip install django djangorestframework python-dotenv supabase "psycopg[binary]"
```

#### 3. Create .env

Create a file named .env in the project root (same folder as manage.py):

DJANGO_SECRET_KEY=change-me
DEBUG=1

##### Supabase Postgres
DB_NAME=xxx
DB_USER=xxx
DB_PASSWORD=xxx
DB_HOST=xxx
DB_PORT=5432

##### Supabase Storage
SUPABASE_URL=xxx
SUPABASE_SERVICE_ROLE_KEY=YOUR_SERVICE_ROLE_KEY
SUPABASE_BUCKET=xxx
SUPABASE_BASE_PREFIX=xxx


#### 4. Run migrations

```zsh
python manage.py migrate
```


### Daily Start

#### Activate venv
```zsh
source .venv/bin/activate
```

#### Run server
```zsh
python manage.py runserver
```

#### Exit venv: 
```zsh
deactivate
```