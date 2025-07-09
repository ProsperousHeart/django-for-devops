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

# [Assign a User with Necessary Permissions](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49870667#overview)

Create an IAM user with the necessary permissions so you can access your bucket with Terraform.

Go back to teh dashboard by clicking the AWS icon in the top left and search for [IAM](https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-2#/home):

![IAM search](/IMGs/section-09/9-IAM-search.png)

You will see a security recommendation come up to enable multifactor authentication:

![AWS security recommendation](/IMGs/section-09/9-AWS-security-rec.png)

Once you have set up your authentication method, it will take you to the [security crednetials screen](https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-2#/security_credentials).

On the IAM screen, go to [users](https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-2#/users):

![IAM users](/IMGs/section-09/9-IAM-users.png)

Click the button to **Create User** - you do not need to provide it access to the management console.

![specify user details](/IMGs/section-09/9-IAM-create-user.png)

Ensure **Permissions options** are set to **Attach policies directly**:

![attach policies](/IMGs/section-09/9-attach-policies.png)

Choose a policy by searching for S3 to get **AmazonS3FullAccess** so we can interact with our S3 bucket:

![choose s3 policy](/IMGs/section-09/9-choose-s3-policy.png)

On the next screen you are just reviewing everything. You can then click on the new user account and go to **security credentials**.

![sec creds](/IMGs/section-09/9-sec-creds.png)

Create an **Access Key** which will allow you to programatically connect to Amazon S3, with permissions ingrained to utilize the S3 to fullest extent.

![access key](/IMGs/section-09/9-access-key.png)

Choose your use case - here `Other` was chosen:

![use case](/IMGs/section-09/9-use-case.png)

Best practices for managing AWS keys can be found [here](https://docs.aws.amazon.com/console/general/access-keys-best-practices):
- Never store your access key in plain text, in a code repository, or in code.
- Disable or delete access keys when no longer needed.
- Enable least-privilege permissions.
- Rotate access keys regularly.

You can move through to complete setup. Copy your access key somewhere safe.

You usually create an IAM group and then assign permissions to the group then go from there.

# [AWS CLI & Credentials Setup](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49870685#overview)

More on this [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

This is how you programatically access AWS. Scroll down the page and choose for your operating system.

## Install the CLI

Download and install the tool.

Open a fresh CMD prompt and run the following to chek that the CLI has been installed:  `aws --version`

Should see something like this:

![confirm AWS CLI installed](/IMGs/section-09/9-AWS-CLI-version.png)

## Configure Access Keys

```
aws configure
```
![configure AWS keys](/IMGs/section-09/9-configure-aws-keys.png)

This likely to look different if adding others, since this is the first time it was set up.