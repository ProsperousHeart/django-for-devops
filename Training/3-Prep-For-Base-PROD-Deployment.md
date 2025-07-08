[Table of Contents](/README.md)

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
