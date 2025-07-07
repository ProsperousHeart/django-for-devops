# django-for-devops
This is the repo I will make as part of my progression through a Udemy course

# Notes to Remember

This comes from [this training](https://www.udemy.com/share/107FCA3@eEZgOBzVh4cfxJVHZypDylXfr0ukjDw_Kk_X553t7XPJ-PHQ0OjD7KOkTXIOruCK/).

You will need to update the `main.tf` file to add the bucket name, GitHub username, etc. This ensures it ties to your specific work and logins. This also applies to the `terraform.yml` in GitHub workflows.

You will also need to update the ENV files.

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

# Dockerization with Django

## What is Docker?

- a software platform used for deploying applications
- apps are **packaged into containers** and can be easily run on any machine & withotu compatibility issues

### How Does Docker Work? (Simplified)

1. create a docker file (list of commands used to assemble a Docker based image)
2. build Docker file while will transform into a Docker image once built
3. push Docker image to a Docker image repository (e.g.:  Docker Hub, Amazon ECR - elastic container registry)
4. pull image from repo then run image (transforms into a Docker container)

## [Installing & Setting Up Docker](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49342619#overview)

https://www.docker.com/products/docker-desktop/

If you are struggling to open Docker Desktop then you most likely will need to install WSL 2 onto your Windows machine.

Here is a FREE video demonstration on how to set it up:

Please only watch up to 2:23 of the video - after you have done so please be sure to restart your computer before you attempt to run Docker Desktop on your machine again

https://www.youtube.com/watch?v=SjdFip4t3kI

## Installing Gunicorn

It bridges the connection between our Django app (which is goign to eb Dockerized) and the servers on teh cloud service provider that we'll be utilizing - Render.

`pip install gunicorn`

## Generating Requirements file

Needed since you ened to specify the dependencies for the Docker file.

`pip freeze > requirements.txt`

Complete command in the main project folder:

![requirements file](/IMGs/section-02/2-Docker-req-file.png)

## [Create a Docker File](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49342637#overview)

A **docker file** is essentially a script that defines how to create a Docker container. It will include a lot of instructions to install dependencies, copy files, set ENV variables, and also define how a container is ultimately going to run.

In base project directory, create:  `Dockerfile`

If using VSCode, it is likely it will install the [Docker extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker).

1. Look for a base Docker image in [Docker Hub](https://hub.docker.com/) - a public registry where we can find & share container images we're utilizing.

2. search for an image (e.g.:  nginx, postgres, [python](https://hub.docker.com/_/python))
![searching images on Docker Hub](/IMGs/section-02/2-Docker-img-search.png)
    - use the official Docker image
    - you'll see the tags start off with version and are followed by some category that give you particular perks unique to each category whens etting up your base image

3. show where the image will come from:  `FROM python:TAG` or `FROM python:VERSION` ... such as `FROM python:3.13`

4. set some default ENV variables to improve performance of our image & avoid unwanted cache files that migth be in place:

    - `ENV PYTHONDONTWRITEBYTECODE=1`:  prevent python from writing **.pyc** files, which reduces storage usage as well
    - `ENV PYTHONBUFFERED`: ensure we have buffering in place, or that python output is immediately sent to terminal (helps debugging logs)
    - additional options VSCode suggested:  `PIP_NO_CACHE_DIR`, `PIP_DISABLE_PIP_VERSION_CHECK`

![Docker ENVs](/IMGs/section-02/2-Docker-ENVs.png)

5. set working dorectory inside our container (location where all of our app files will be stored):  `WORKDIR /app`

6. copy requirements file into container from base directory - allows to isntall dependencies before copying full app (helps to improve caching):  `COPY requirements.txt .`

7. upgrade pip to latest version:  `RUN pip install --upgrade pip`

8. install all dependencies listed in requirements file: `RUN pip install -r requirements.txt`

9. copy all project files into container - will include Django app code, static files, template, etc (everything from our directory) into the working directory of the container:  `COPY . .`

10. Expose port so application can be accessed from outside the container:  `EXPOSE 8000`

11. set default command that's going to run when our container starts:  `CMD [list of commands to utilize gunicorn]`

    - most people use comment `python manage.py runserver` but it's better to utilize Gunicorn or gvicorn when you're working with PROD ENVs
    - `--bind` binds application to all network interfaces available on the 3rd input (post 8000)
    - runs **gunicorn** server instead of default
    - specify Django application entry point so we can interact with our Django app and ensure it will run on the cloud server we choose:  `projectname.wsgi:application` (which is found in project `settings.py` file as variable **WSGI_APPLICATION**)
    - (OPTIONAL) define worker process that will help handle multiple requests more efficiently (optimize performance):  `"--workers=3"`
    - VSCODE kind of suggested these but not in this way:  `"--timeout=120", "--log-level=info"`

    NOTE:  what is seen in the CMD is the entire command being put into the "command prompt" when run

## [Add a Docker Ignore File](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49342641#overview)

Important if we want to ensure that we don't go ahead and install certain parts of our app that don't need to be installed within our Docker file.

In main project directory, create:  `.dockerignore`

```docker
Dockerfile
.dockerignore
```

## [Build Docker Image](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49342645#overview)

Navigate to your terminal / CMD within your virtual environment. Run:  `docker build -t IMAGENAME .`

You create a **tag** using `-t IMAGENAME`

The `.` tells Docker to look for Docker file in our current directory specified.

![Docker build outcome](/IMGs/section-02/2-Docker-build.png)

You can now see the image in local Docker desktop.

![builds on desktop](/IMGs/section-02/2-Docker-desktop-builds.png)

## [Run a Docker Container](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49342653#overview)

Need to transform the image into a Docker container:  `docker run -d -p CONTAINER_PORT:COMPUTER_PORT IMAGE_NAME_TO_RUN`

Create and start container from an image:  `docker run`

Run container in detached mode (so logs don't show in terminal):  `-d`

Map port binding to 8000 from container to our computer so we cna access the application in our browser.

Full line: `docker run -d -p 8000:8000 django-app`

You will receive the image ID back:

![returned image ID](/IMGs/section-02/2-Docker-image-ID.png)

You can view the running container in Docker desktop:

![Docker desktop running container](/IMGs/section-02/2-Docker-running-container.png)

- green icon indicates in use
- can see image base name
- see it's on the expected ports and clicking it

Ran into [this issue](https://github.com/docker/for-win/issues/14327) and updating Docker resolved it.

## [Docker Resource Cleanup](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49342951#overview)

Stop & delete the container. Delete the image.

There is a build cache that is persistent - must run the following in CMD prompt:  `docker system prune`

![what docker prune covers](/IMGs/section-02/2-Docker-pruning.png)

What happens usually is when you run Docker build it's going to save you time the next build because it will cache everything that hasn't been changed in your application.

# Preparing for Base PROD Deployment

## Installing psycopg2-binary

To install [psycopg2-binary](https://pypi.org/project/psycopg2-binary/) run:  `pip install psycopg2-binary`

## [Add Markup for PROD Database](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49342801#overview)

Adding in markup so we can go to our `settings.py` file of main app section - by default using SQLite database:

![default DB](/IMGs/section-03/3-default-db.png)

Now we'll create the markup for our PROD database, which will be based on a Postgres DB.

![markup for postgres prep](/IMGs/section-03/3-markup-for-postgres.png)

## [Configure ENV variables](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49342863#overview)

Many ways to do this - libraries, packages, etc ... But recommended to use [django-environ](https://pypi.org/project/django-environ/) - check out the [READTHEDOCS](https://django-environ.readthedocs.io/en/latest/)! It allows you to do the [12 factor](https://www.12factor.net/) process.

It's a simple and effective package we can use for setting up our ENV vars. Install by running:  `pip install django-environ`

In your project, add a new file:  `.env`

This will house our application's environment variables (secret key, DB settings, etc) ... shoudl be added to `.gitignore` for safety reasons.

Go to main project app's `settings.py` and review what might be sensitive:
- `SECRET_KEY`

Ensure you import `environ` & initialize at the top:

Then you want to read the `.env` file (in root directory)

![implement environ](/IMGs/section-03/3-implement-environ.png)

Ensure you store sensitive information in the ENV file so we can work with them with our files in local development for now.

In the ENv file:  `SECRET_KEY=django-insecure-un)v0ke+fwp0d+&p#(w6!nx&df=o4%2(^96qa$c6+(c7ij=@%(` (no quotes or spaces)

Update the `settings.py` file so it pulls the ENV var:  `SECRET_KEY = env("SECRET_KEY")`

## [Additional Deployment Configurations](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49342937#overview)

Additional settings in teh `settings.py` file of main project app

Set `DEBUG` to false ... or better yet have it be updated in your ENV vars

Under `ALLOWED_HOSTS`, of course we are deployed & everything we want to grab & connect to the domain available to us (in this instanc it will be from render)

To ensure we don't have any issues, because we can't guess what the URL is going to be, we'll just add the star:  `ALLOWED_HOSTS = ["*"]`
As we get a relvant domain name or URL we're going to change it to that so we have even better pratices / policies followed.

Nest we set up CSRF trusted origins. This will ensure we can make POST requests on our domains on our server with that particular domain name with that URL we have https:  `# CSRF_TRUSTED_ORIGINS = ['']`

Leave empty for now.

These are now in place for when we're ready!

## [Handling static assets with WhiteNoise](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49342931#overview)

We want to be able to work with our static files (CSS, JS) & all behind the scenes files we don't see but work with all the time. Need to ensure we can utilize it in PROD.

[Whitenoise](https://pypi.org/project/whitenoise/) ReadtheDocs [here](https://whitenoise.readthedocs.io/en/latest/). It's a specific package you can use to allow you to serve your static files in PROD.

Configure it per [here](https://whitenoise.readthedocs.io/en/stable/django.html#make-sure-staticfiles-is-configured-correctly).

Enable it via `MIDDLEWARE` just below the security by adding:  `"whitenoise.middleware.WhiteNoiseMiddleware",`

Add compression & caching support for optimal performance. So no matter what browser is viewing, it's not going to run into a situation where it will cache your app static files because browsers do that ... then you don't always get the latest version.

By adding compression & caching support it'll hash your files to ensure they forcibly load the latest updates to said static files. This requires setting the root directory as outlined in step 1. Will house all static files for the app.

The code goes in the main app's `settings.py` file.

![static files setup](/IMGs/section-03/3-static-section.png)

Thsi will look for the `staticfiles` folder which will be created.

After configuration, run the following to get the files copied to the expected folder:  `python manage.py collectstatic`

![created static folder](/IMGs/section-03/3-static-folder-creation.png)

All has CSS files and more - the most important file is `staticfiles.json` and it should have been automatically created. (provides caching support for entire app)

### How to Test

1. make sure your server is running

2. view page source after refresh

# GitHub Container Registry

## [What is a Container Registry?](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49342745#overview)

**container registry** - storage system for container (docker) images, the blueprints of apps that run in containers

Popular registries include:
- Amazon ECR
- GitHub Container Registry
- Google Artifact Registry
- Azure Container Registry

Simple way to see registries as GH repos for source code but for Docker images.

## Generate a PAT

Go to the [classic token](https://github.com/settings/tokens) and create one.

![generate PAT](/IMGs/section-04/4-Generate-PAT.png)

We want to build a Docker container locally and push to GH container registry.

NOTE:   Docker Image Permissions

Scope to/from packages registry:
- write packages
- delete packages

Can treat a package as a docker image.

Only visible to you once so be sure you copy the key.

## Login to GH Container Registry

In CMD prompt:  `docker login ghcr.io --username USERNAME --password PAT`

Since using locally, the warning is ok.

![GHCR login](/IMGs/section-04/4-login-GHCR.png)

## [Updating Packages & Ignoring ENV](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49343651#overview)

Ensure `.env` is ignored to ensure no sensitive information is exposed in our Docker image

Also want to ensure we're using the latest packages

1. In CMD prompt:  `pip freeze > requirements.txt`

2. Update `.dockerignore` with:  `.env`

## Ignoring additional files/directories - [Important]

Hi all,

Please note that you can also add your **staticfiles** directory into `.dockerignore` by stating `staticfiles/`

This is optional, but I'd strongly recommend that you do so since we already run collectstatic with our entrypoint.sh file to generate fresh staticfiles with each deployment and because we want to clean up our code.

That being said, you can do that for now or you can wait until later lectures where we will do a full source code cleanup.

Best,
Arno

## [Build a Docker Image for PROD](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49343047#overview)

This is where we'll build a Docker image in PROD, so we'll tidy things up and ensure we can handle our static files & migrations.

Best way is to create an `entrypoint.sh` script in project's base directory.

This will run when our Docker container starts - **at run time**. It will then execute all commands in there.

1. Need to add **shebang line** (tells our system to run the script with bash):  `#!/bin/bash`

2. **echo** will act as the output command - logging for the server:

    - `echo "Running migrations..."`
    - `python manage.py migrate --noinput` (don't want user to prompt y/n ... want terminal to automatically run this command for us)
    
3. collect static files:
    - `echo "Collecting static files..."`
    - `python manage.py collectstatic --noinput`

4. execute gunicorn here instead of the Dockerfile:

    - remove or comment out from the main project's Dockerfile:  `CMD ["gunicorn", "--bind", "0.0.0.0:8000", "edenthought.wsgi:application", "--workers=3"]`

    - rewrite the command in the entrypoint file:
    `exec gunicorn PROJECTNAME.wsgi:application --bind 0.0.0.0:8000 --workers 3`
        - `exec` for execution
        - project name before bind

5. update Dockerfile so it refers to the entrypoint & ensure it's runnable: `RUN chmod +x ./entrypoint.sh` (will ensure the file is executable & `.` is referring to the *WORKDIR*)

6. Set up your entry point:  `ENTRYPOINT ["PATH_TO_RUN_FILE"]`

![update gunicorn](/IMGs/section-04/4-update-gunicorn-loc.png)

The entrypoint tells container to run the script when container starts.

## Docker Build Command (WIN)

`docker build -t gfcr.io/lowercaseusername/pkgname-for-ghcr .`

![GHCR image](/IMGs/section-04/4-ghcr-image.png)

## [Push Docker Image to GHCR](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49343099#overview)

If you've logged into GHCR you should be able to run:  `docker push ghcr.io/username/image-name:tag`

While items are being pushed, you'll see something like this:

![GHCR docker image push in progress](/IMGs/section-04/4-ghcr-img-push-in-progress.png)

One completed, you'll see the latest SHA and size:

![GHCR pushed IMG SHA256](/IMGs/section-04/4-ghcr-pushed-img-sha.png)

You can see your package under your GitHub profile such as [here](https://github.com/ProsperousHeart?tab=packages).

# Cloud Service Models & Strategy

## Service Models

1. **IaaS (Infrastructure as a Service)**:  provides VMs, storage, & networking allowing users to manage their own software while the cloud provider handles the hardware (e.g.:  AWS EC2)

![IaaS](/IMGs/section-05/5-cloud-service-IaaS.png)

2. **PaaS (Platform as a Service)**:  offers a pre-configured platform for developing, running, & managing applications without worrying about underlying infrastructure (e.g.: Render, Heroku, Railway, AWS Elastic Beanstalk) ... simplest way to deploy your app!

![PaaS](/IMGs/section-05/5-cloud-service-PaaS.png)

3. **IaC (Infrastructure as Code)**:  automates cloud resource provisioning & management using code

![IaC](/IMGs/section-05/5-cloud-service-IaC.png)

## Use Case 1:  PaaS

![use case 1](/IMGs/section-05/5-cloud-service-use-case-1.png)

## Use Case 2:  IaC

**Terraform** is an infrastructure as code tool. We'll utilize it so we can write the necessary code & communicate with render, so we can setup the resources to be provisioned based on the code we write with Terraform.

![use case 2](/IMGs/section-05/5-cloud-service-use-case-2.png)

# PaaS with Render

## Intro & Setup of Render

Render is a cloud service provider like heroku, AWS, Azure, Google Cloud, etc. We'll use this for the course and focus mainly on IaC & ensure we have a nice DevOps CICD process.

## Deploy A Dockerized App with Render

Navigate to your projects [dashboard](https://dashboard.render.com/).

Choose to add a [new web service](https://dashboard.render.com/web/new).

![add PaaS web service](/IMGs/section-06/6-PaaS-Render-add-web-service.png)

Choose existing image:

![choose existing image](/IMGs/section-06/6-PaaS-web-svc-choose-existing.png)

Paste your URL, such as from one of you GHCR items [here](https://github.com/users/ProsperousHeart/packages/container/package):  `docker pull ghcr.io/prosperousheart/app-image:latest`

If it's private, you'll need to add your PAT as a [registry credential](https://render.com/docs/deploying-an-image#managing-credentials).

![add cred alert](/IMGs/section-06/6-alert-to-add-cred.png)

![add cred screen - empty](/IMGs/section-06/6-add-cred-screen.png)

Registry will be GitHub and this is where you'll use the PAT that was made.

![add cred screen - complete](/IMGs/section-06/6-add-cred-screen-complete.png)

You will now be able to use that credential:

![final existing image](/IMGs/section-06/6-final-existing-img.png)

Click the **connect** button. You can then update the following ...

![alt text](/IMGs/section-06/6-new-svc-1.png)

Choose the free instance.

![alt text](/IMGs/section-06/6-new-svc-2.png)

Add your ENV variables into Render.

![alt text](/IMGs/section-06/6-new-svc-3.png)

Then choose the **Deploy Web Service** when ready.

## [Additional Config & Updating Our App](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49548439#overview)

Go to your main app's `settings.py` file.

Set the `ALLOWED_HOSTS` to the domain name given by Render - be sure to remove the `https://`.

![update ALLOWED_HOSTS](/IMGs/section-06/6-allowed-domains-update.png)

Set your `CSRF_TRUSTED_ORIGINS` - it will be the entire URL from before. This will allow you to make POST requests effectively.

Run the build and push lines again - for this example:

```
docker build -t gfcr.io/prosperousheart/app-image .
docker push ghcr.io/prosperousheart/app-image:latest
```

Once pushed, go back to Render and tell it to deploy latest reference.

![deploy latest](/IMGs/section-06/6-deploy-latest-ref.png)

Once deployed, you can tests if CSRF is working if the POST completed and the list is updated.

## [Create & Integrate PostgreSQL DB for PROD](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49548465#overview)

Was going to hold off untilIaC lessons, but important to have fundamental understanding of hwo it's done manually.

1. Add new Postgres service in Render

2. Set up your new instance - make sure it's in the same region as the website

    Now it's time to set up as i was prepped in our Django app. Can do thsi while it's setting up - includign secret keys.

1. comment out the SQLite DB

2. uncomment out the postgres portion & update to what is in Render

    ![swap databases](/IMGs/section-06/6-swap-dbs.png)

3. In the video, he started by updating the `settings.py` file first:

    ![settings file update with render data](/IMGs/section-06/6-swap-dbs.png)

4. ensure connected to new DB:    `python manage.py runserver`

    If it tells you migrations are needed, you're good to go.

    ![no migrations](/IMGs/section-06/6-no-migrations-needed.png)

    You might also run into a 400 error. This is due to CSRF and you'll need to update the settings as such:

    ![alt text](image.png)

5. make migrations:  `python manage.py migrate`

6. create superuser for PROD:  `python manage.py createsuperuser`

    In this example `adminprodtest` was used as username.

    When we switch to postgres (PROD) DB, all of the data created from now on will be stored in this DB. You won't see the data you had before.

7. open your ENV file and add the appropriate information for the sections to be filled out

8. run Docker command from before:

    ```
    docker build -t ghcr.io/prosperousheart/app-image .
    docker push ghcr.io/prosperousheart/app-image:latest
    ```

9. Go back to the web app on Render and access the environment variables. Then put them in form your local ENV file.

    But be mindful of the hostname! Using the same from the ENV file like this will be wrong as it is external:

    ![Render ENVs](/IMGs/section-06/6-envs-on-render-bad.png)

    You should use the hostname that is given for internal items like this:

    ![Render ENVs](/IMGs/section-06/6-envs-on-render-good.png)

    Once configured, hit save & deploy. You can see progress in the events or logs section on your service dashboard.

    In the event it's not using the latest image, update it!

## [Resource Cleanup](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49548469#overview)

Delete your package from GitHub.

In settings dashboard for your web app, delete the web service.

Delete the database on Render.

Go to your Render workspace settings & remove GitHub credential. (We'll return later.)

Comment out postgres DB info and uncomment SQLite

clear up ENV file:

![alt text](/IMGs/section-06/6-clear-up-env-from-postgres.png)

clear up `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`:

![allowed and trusted](/IMGs/section-06/6-clean-up-allowed-hosts-csrf.png)

