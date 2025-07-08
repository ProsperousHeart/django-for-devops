[Table of Contents](/README.md)

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
