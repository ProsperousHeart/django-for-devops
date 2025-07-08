[Table of Contents](/README.md)

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
