# 147 Drum Machines API (Django)

Backend API for **147 Drum Machines**.
- Django + Django REST Framework

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
python -m pip install django djangorestframework python-dotenv "psycopg[binary]"
```

#### 3. Create .env

Create a file named .env in the project root (same folder as manage.py):

DJANGO_SECRET_KEY=change-me
DEBUG=1



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