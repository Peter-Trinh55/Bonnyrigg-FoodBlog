# Bonnyrigg High School Food Blog (Flask)

## Project Overview
A recipe-focused food blog for the Bonnyrigg High School community. Users can register, submit recipes, browse/filter/search, and comment. Admin users can moderate content.

## Key Features
- User accounts (register/login/logout)
- Recipes with: title, image, summary, ingredients, instructions, cook time, difficulty, cuisine, tags
- Search & filtering (keyword, cuisine, difficulty, max cook time, ingredient keyword, tag)
- Comments on recipe pages
- Admin dashboard for recipe management + comment moderation + tag management
- SQLite database with SQLAlchemy ORM
- Validation with Flask-WTF + CSRF protection
- Safe image uploads (restricted extensions + renamed files + resized images)
- Error pages (403/404/500)

## Tech Stack
- Flask, Jinja2
- SQLite + SQLAlchemy ORM
- Bootstrap 5
- Flask-Login, Flask-Bcrypt, Flask-WTF
- Pillow (image resizing)

## Installation & Running
1. Create and activate venv
2. Install requirements
3. Run the server

### Windows (PowerShell)
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py

## Test Data & Screenshots
This project includes seed scripts to populate the database with example content
for testing and assessment screenshots.

### Seed scripts
```powershell
python seed.py
python seed_more.py
