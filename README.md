# elcompressor

<img alt="logo" height="200" src="static/home/assets/compress_logotype.png" width="200"/>

## Description

This Django project is designed to automate image compression. elcompressor is a tiny Django Saas that allows you to compress your images in a few clicks. It is based on a custom algorithm. 
This script also comes with an API that allows you to compress your images directly from your website.

## Requirements
- Python 3.10
- Django 4.2.3
- TailwindCSS
- AlpineJS
- HTMX
- Stripe account
- Brevo (Sendinblue) account

## Installation
- Clone the repository
- Install dependencies with `pip install -r requirements.txt`
- Setting up environment variables:
    - Copy the `.env.dist` file to `.env`
    - Fill in the environment variables in the `.env` file
- Run the migrations with `python manage.py makemigrations` and `python manage.py migrate`
- Create a superuser with `python manage.py createsuperuser`
- Run the server with `python manage.py runserver`

## Usage
- The script is designed to be easily reproducible

