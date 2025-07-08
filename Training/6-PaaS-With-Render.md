[Table of Contents](/README.md)

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