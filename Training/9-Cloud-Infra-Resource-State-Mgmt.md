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

# [Create & Setup S3 Bucket](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49870661#overview)

Search for [S3](https://us-east-2.console.aws.amazon.com/s3/get-started?region=us-east-2) in the search bar of your [Management Console](https://us-east-2.console.aws.amazon.com/console/home?region=us-east-2#).

![s3 search](/IMGs/section-09/9-s3-search.png)

Click the "[Create bucket](https://us-east-2.console.aws.amazon.com/s3/bucket/create?region=us-east-2&bucketType=general)" button:

![create bucket](/IMGs/section-09/9-create-bucket.png)

Region will be auto assigned based on what your profile has in the top right.

We'll leave as a **General purpose** bucket so give it a name, like:  `my-terraform-bkt-96`

Leave object ownership as default with ACLs disabled.

Ensure the **Block Public Access settings** is blocked for ALL.

Recommended to enable **Bucket Versioning** as it is helpful if our Terraform state file changes and you need to rollback to an earlier one.

Encryption is enabled by default.

When you create your bucket, you'll see a screen similar to:

![bucket made redirect screen](/IMGs/section-09/9-bucket-made.png)

