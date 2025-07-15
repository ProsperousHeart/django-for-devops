[Table of Contents](/README.md)

# [General & Basic Monitoring with Render](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49344687#overview)

When you go to your Render web app, on the left hadn side is a section for `MONITOR`. You can filter your logs as well as other things (e.g. timeframe, sorting, etc).

Same with metrics section.

# [Resource Cleanup](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49926403#overview)

## Render

Delete service at bottom of each Render application.

Go to workspace settings and delete container registry credentials.

In Render account settings, delete (revoke) API key.

## AWS

Open **IAM** then under access management > users > choose a user > security > Access Keys:
1. deactivate your access keys
2. delete your access keys
3. delete the user created

Access **S3** and delete the Terraform state:
1. choose bucket & empty it (`permanetnly delete`)
2. delete the bucket

## GitHub

You can go to the repo settings, all the way down and delete it - including the ENV vars and Actions.

Profile icon > settings > developer settings > personal access tokens > classic tokens > delete your PAT

You can delete the Docker image in the package section.