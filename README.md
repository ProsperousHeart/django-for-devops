# django-for-devops
This is the repo I will make as part of my progression through a Udemy course

# Notes to Remember

This comes from [this training](https://www.udemy.com/share/107FCA3@eEZgOBzVh4cfxJVHZypDylXfr0ukjDw_Kk_X553t7XPJ-PHQ0OjD7KOkTXIOruCK/).

You will need to update the `main.tf` file to add the bucket name, GitHub username, etc. This ensures it ties to your specific work and logins. This also applies to the `terraform.yml` in GitHub workflows.

You will also need to update the ENV files.

# Setup

## New Project

Set up venv and install `django`. Run:  `django-admin startproject` in the folder that will be the aprent that your main project folder will live in.

Change into the new directory and run:  `python manage.py runserver`

## Setup The App

Before making the app, do the initial default migrations. Run:  `python manage.py migrate`

This will migrate all of the default apps in Django app & push those DB files into place. You can see the apps were installed by reviewing the `settings.py` file in `INSTALLED_APPS`.

Create the app using:  `django-admin startapp crm` (name of app)

![CRM App Added](/IMGs/1-crm-setup.png)

Add the app to the installed apps:

![add CRM to installed apps](/IMGs/1-crm-initialization.png)

Rerun server to ensure it's still working.