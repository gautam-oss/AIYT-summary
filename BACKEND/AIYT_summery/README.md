# Django YouTube to Blog Generator

This is a Django application that uses OpenAI's API to generate blog posts from YouTube video transcripts.

## Features

*   User authentication (signup, login, logout)
*   Generate blog posts from YouTube video links
*   Save generated blog posts
*   View all saved blog posts
*   View blog post details

## Setup Instructions

These instructions will guide you through setting up the project for development on your local machine.

### 1. Prerequisites

*   Python 3.8 or higher
*   pip (Python package installer)
*   A text editor or IDE (e.g., VS Code, PyCharm)

### 2. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies. Open your terminal or command prompt and navigate to the project's root directory.

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate

# On macOS and Linux
source venv/bin/activate
```

### 3. Install Dependencies

Install all the required packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

This project uses a `.env` file to manage environment variables. Create a `.env` file in the project root directory by copying the `.env.example` file.

```bash
# On Windows
copy .env.example .env

# On macOS and Linux
cp .env.example .env
```

Now, you need to fill in the required values in the `.env` file.

*   `SECRET_KEY`: A secret key for a particular Django installation. You can generate a new one using an online generator or by running the following Python code:

    ```python
    from django.core.management.utils import get_random_secret_key
    print(get_random_secret_key())
    ```

*   `OPENAI_API_KEY`: Your API key from OpenAI.

#### How to get an OpenAI API Key

1.  Go to the [OpenAI website](https://openai.com/).
2.  If you don't have an account, sign up for one.
3.  Once you are logged in, navigate to the API section.
4.  You should be able to find your API key in your account settings. It will be a long string of characters starting with `sk-`.

### 5. Run Database Migrations

Apply the database migrations to create the necessary tables.

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run the Development Server

Start the Django development server.

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.

## Common Troubleshooting

*   **`ModuleNotFoundError: No module named '...'`**: This usually means a required package is not installed. Make sure your virtual environment is activated and run `pip install -r requirements.txt` again.

*   **`django.db.utils.OperationalError`**: This can happen if the database is not set up correctly. Ensure you have run the migrations. If you are using a database other than SQLite, make sure the database server is running and the credentials in your `settings.py` are correct.

*   **OpenAI API Errors**: If you are getting errors related to the OpenAI API, double-check that your `OPENAI_API_KEY` is correct and that you have sufficient credits in your OpenAI account.

*   **CSRF Errors**: If you encounter CSRF (Cross-Site Request Forgery) errors, ensure that you have added your development domain to `CSRF_TRUSTED_ORIGINS` in your `settings.py` file (e.g., `CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000']`).

## Django Migration Commands

Here are the common Django migration commands for both Windows and Linux/macOS.

### Create and Apply Migrations

When you make changes to your models (e.g., `models.py`), you need to create a migration file and then apply it to the database.

```bash
# Create migrations for the BlogArticle model
python manage.py makemigrations summery_generator

# Apply migrations to the database
python manage.py migrate
```

### Create a Superuser

To access the Django admin panel, you need to create a superuser.

```bash
python manage.py createsuperuser
```

Follow the prompts to create a username, email, and password.

### Check Migration Status

You can check the status of migrations to see which ones have been applied.

```bash
python manage.py showmigrations
```

### Rollback Migrations

If you need to undo a migration, you can roll it back. To roll back to a specific migration, you can specify the migration name. To roll back all migrations for an app, you can use the `zero` keyword.

```bash
# Roll back the last migration for the summery_generator app
python manage.py migrate summery_generator <migration_name>

# Roll back all migrations for the summery_generator app
python manage.py migrate summery_generator zero
```

### Handling Migration Conflicts

Migration conflicts can occur when working in a team. If you have conflicting migrations, you may need to reset the migrations for a specific app.

**Warning:** This will delete the migration history for the app from the database. It does not delete the tables or data.

```bash
# 1. Delete the migration files in the app's migrations directory (but not the __init__.py file)

# 2. Clear the migration history for the app from the database
python manage.py migrate --fake summery_generator zero

# 3. Create new migrations
python manage.py makemigrations summery_generator

# 4. Apply the new migrations
python manage.py migrate --fake-initial
```

### Resetting the Database

If you want to completely reset your database (delete all tables and data), you can do the following:

**Warning:** This is a destructive operation and will delete all your data.

```bash
# 1. Delete the SQLite database file (db.sqlite3)
# On Windows
del db.sqlite3

# On macOS and Linux
rm db.sqlite3

# 2. Re-run migrations
python manage.py migrate
```