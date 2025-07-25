[Table of Contents](/README.md)

# App Setup

## New Project

Set up venv and install `django`. Run:  `django-admin startproject` in the folder that will be the aprent that your main project folder will live in.

Change into the new directory and run:  `python manage.py runserver`

## Setup The App

Before making the app, do the initial default migrations. Run:  `python manage.py migrate`

This will migrate all of the default apps in Django app & push those DB files into place. You can see the apps were installed by reviewing the `settings.py` file in `INSTALLED_APPS`.

Create the app using:  `django-admin startapp crm` (name of app)

![CRM App Added](/IMGs/section-01/1-crm-setup.png)

Add the app to the installed apps:

![add CRM to installed apps](/IMGs/section-01/1-crm-initialization.png)

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

## [Create & Register Django Model](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49342589#overview) (Daily Note)

Users will be able to add in notes of their day.

1. go to CRM app `models.py` file
2. define the model - essentially a DB table ... to create own model:
    - pass in `models.model`
    - define attributes and fields

```python
class DailyNote(models.Model):
    title = models.CharField(max_length=100)
```

3. make your migrations - allow Django to create a mock up or backbone structure of daily note model by running `python manage.py migrate`

![1st DB update](/IMGs/section-01/1-makemigrations.png)

Now it's available in our CRM app under a migrations folder:

![Migration Folder Creation](/IMGs/section-01/1-migration-outcome.png)

4. then push it to our SQLite DB or our default DB using:  `python manage.py migrate`

![Push Migration to DB](/IMGs/section-01/1-migration-push-to-db.png)

5. to access the model, must import it into app's `admin.py` file:

```python
# CRM admin.py
from . models import DailyNote
```

6. to access the model, must register in Django admin ... go to app's `admin.py` file 

![Register new model](/IMGs/section-01/1-register-model.png)

## Accessing Django Admin

Create super user:  `python manage.py createsuperuser`

Start server:  `python manage.py runserver`

Access Django Admin:  http://127.0.0.1:8000/admin

![Django Admin](/IMGs/section-01/1-django-admin.png)

![DailyNote admin](/IMGs/section-01/1-admin-dailynote.png)

## Build Basic Form for Submitting Notes

### Part 1

Add `forms.py` file in CRM app where we'll add in our code to build this bsaic form.

In this new file, import `forms` module - provides classes & tools for creating/handling forms within a Django application

```python
from django import forms
```

Import **DailyNote** model from our curent app's `models.py` file - represent the data structure our form will interact with.

```python
from . models import DailyNote
```

Declare **DailyNote** form - it will be a class that inherits from `forms.ModelForm` (a Django class specifically designed for creating forms directly tied to models -- form fields will be automatically generated based on form fields).

Create a nested class inside `DailyNoteForm`. Will be used to define metadata for our DailyNoteForm class - specifying how it should behave or interact with our associated model.

    Specify the model you're working with.

    Specify fields you're using. If you have multiple, separate by comma.

```python
class DailyNoteForm(forms.ModelForm):

    class Meta:
        model = DailyNote
        fields = ['title']
```

Build upon previously created **View**.

### Part 2

Import `DailyNote` model and `DailyNoteForm` in the `views.py` file.

```python
from . models import DailyNote
from . forms import DailyNoteForm
```

Check if the request is going to be a POST we are expecting/working with & assign the `DailyNoteForm` to a variable. We intend for the data entered in the fields of that form be sent as a POST request. Ensure to check if the form is valid, without any errors or issues.

```python
def home(request):
    """
    Render the home page of the CRM application.
    
    Args:
        request: The HTTP request object.
    
    Returns:
        HttpResponse: Rendered home page template.
    """

    if request.method == 'POST':
        form = DailyNoteForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request, 'index.html')
```

To redirect to home page, must import `redirect` from `django.shortcuts` and add in-line to validation section:

```python
def home(request):

    if request.method == 'POST':
        form = DailyNoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'index.html')
```

If not a POST request, simply assign form without the input:  `form = DailyNoteForm()` (shows a blank form each tiem you try to access the `index.html` page without wanting to make a post)

```python
def home(request):

    if request.method == 'POST':
        form = DailyNoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DailyNoteForm()

    return render(request, 'index.html')
```

In line of final render, perform query to obtain all objects within the DailyNotes model. Then set up a dictionary so we can output our form and all notes to the `index.html` page. The keys are what will reference in your HTML & the values are what you set to the key.

In this instance:
- the form
- the notes

```python
def home(request):

    if request.method == 'POST':
        form = DailyNoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DailyNoteForm()
    
    notes = DailyNote.objects.all()
    return render(request, 'index.html', {'myForm': form, 'notes': notes})
```

Update the HTML page to be able to include the data.

When passing in data in Django via POST request, we need to pass through a CSRF token for protection. Then pass in your form using double braces. (adding `.as_p` gives some styling)

To trigger the POST statement need a button. Once clickedn that line of code just mentioned will be instantiated.

```html
<html>
    <head>
        <title>Daily Notes</title>
    </head>
    <body>
        <h1>Welcome to DailyNotes!</h1>
        <hr/>>
        <h3>Add a new note:
        <form method="post">
            {% csrf_token %}
            {{myForm.as_p}}
            <button type="submit">Add note</button>
        </form>
</html>
```

We also want the form to be displayed on this HTML. We want to see all notes on the home page. Should be done outside the form section.

Set up unordered list! Use for loop to traverse notes.

```python
        {% if myNotes %}
            <ul>
                {% for note in myNotes %}
                    <strong>{{note.title}}</strong>
                {% endfor %}
            </ul>
        {% else %}
            <p>No notes available.</p>
        {% endif %}
```

## Configure Static Files

Create `static` folder in base directory:

![static folder](/IMGs/section-01/1-static-folder.png)

Navigate to main project's `settings.py` file and go to the `STATIC_URL` location. Here we will tell Django where to serve static files from - add the `STATICFILES_DIRS` like so:

![STATICFILES_DIRS](/IMGs/section-01/1-static-files-dirs.png)

## [Setup CSS & JS files + Testing](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49342601#overview)

Create a CSS and JS folder in your `static` folder. (lower case?)

Create a `styles.css` file in your `css` folder.

At the top of your HTML file, load your static:  `{% load static %}`

Integrate your styles file into your index HTML file:  `<link rel="stylesheet" type="text/css" href="{% static 'css/style.css' %}">` (he didn't include the type)

Create JS file in the `js` folder.

Write your JS code. Need to reference according to an ID. In this case we want to be set according to our form. We will want to modify our form.

Put an ID in the POST portion of HTML file:  `<form id="note-form" method="post">`

We want an alert to show if it was added successfully -this will be done in the JS file.

You will create a function that will start "on submit" when the element ID is utilized. The `event.preventDefault()` ensures the event will trigger but not occur on default - triggered on submission.

When submit done, want to show alert.

```javascript
document.getElementById("note-form").onsubmit = function(event) {
    event.preventDefault(); // Prevent the default form submission

    alert("Your not was added!");
    this.submit();
}
```

To ensure we're able to run this JS, best practice to ensure you add this in right below your code in index file near end outside of body.

`<script src="{% static 'js/app.js' %}"></script>`

## [Apply Styling To Form](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49342603#overview)

Go to **static** folder to open CSS file. Add you `note-form` id to it & others. Likely need to delete cache and restart server to see changes.
