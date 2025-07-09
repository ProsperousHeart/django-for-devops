[Table of Contents](/README.md)

# [Create AWS Account](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49870649#overview)

[AWS site](https://aws.amazon.com/free)

Reason we need an AWS account is because we want to utilize Amazon S3 service so we can effectively store & manage our infrastructure as code resource state. (Specifically pertains to Terraform state file - which houses the state of our infrastructure.)

Need to ensure we keep using the same stateused when building our infra. (Use the same blueprint.)

Once you sign up, the will most likely use [AWS Management Console](https://us-east-2.console.aws.amazon.com/console/home?region=us-east-2#) the most.

# [Amazon S3 (Theory)](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49870657#overview)

**Amazon S3** allows you to store your **objects (files)buckets (directories)**.

All bucket names must be unique across the world.

You can use S3 to store any file time you want - commonly user images or static files.

Thsi is one of the main buliding blocks of AWS. It is a core service offered.

Can be used for:
- backup & storage
- hosting static websites
- disaster recovery

## How It Works (Simplified)

![how AWS works SIMPLE](/IMGs/section-09/9-how-aws-works-simple.png)

