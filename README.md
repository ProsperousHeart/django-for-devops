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

## Create Base Template & View

Will use app level template rendering instead of project level template rendering, which is usually configured in our templates list in the `settings.py` file.

1. go to app folder
2. create new `templates` folder
3. create an `index.html` template file & start it
4. create `urls.py` file in the app
5. configure `urls.py` within CRM app with our main `urls.py` project file for EdenThought -- duplicate from original!
6. make sure URL routings are in place so you can connect all the URLs in CRM app are linked to main project ... utilize `include` function and have comma at the end

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('crm.urls')),  # Include the CRM app's URLs
]
```

7. configure CRM `urls.py` file but can borrow logic. Need to utilize our path function:  `from django.urls import path`
8. to be able to access your `views.py` file will need to import
9. add `urlpatterns`

```python
# CRM urls.py
from django.urls import path
from . import views

urlpatterns = [
]
```

10. open `views.py` in CRM app and create a sample view that returns the CRM's rendered template

```python
from django.shortcuts import render

def home(request):
    """
    Render the home page of the CRM application.
    
    Args:
        request: The HTTP request object.
    
    Returns:
        HttpResponse: Rendered home page template.
    """
    return render(request, 'index.html')
```

11. set up the path in your CRM `urls.py` file

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
```

12. test it out by running:  `python manage.py runserver`

## [Create & REgister Django Model](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49342589#overview) (Daily Note)


