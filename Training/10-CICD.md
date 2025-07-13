[Table of Contents](/README.md)

# What is the Definition of DevOps?

**DevOps** - the intersection of development and operations

**development** and **operations** are 2 main components that form  part of the entire **application release process**

DevOps is an organizational approach that promtes collaboration & communication between dev and ops teams to improve overall efficiency in delievering software.

Automation in DevOps streamlines repetitive tasks, improving consistency throughout the SDL.

# [What is CI/CD and How Can We Utilize It?](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49880173#overview)

**What is CICD?** In DevOps, it is a process that automates building, testing, and deploying code, so updates reach users quicker & more reliably.

It encourages teamwork, automates repeated tasks, and shortens time that it takes to release new bug fixes or features.

Also helps team respond quickly to user feedback, making it easier to continuously improve the product.

**Continuous Integration (CI)** - developers regularly add code to a shared space & automated checks make sure it all works together.

**Continuous Deployment (CD)** - once the code passes tests, it's automatically deployed to production, delivering updates to users without manual intervention

CI/CD automates the process of integrating, testing, and deploying code, ensuring seamless updates & delivery to users automatically.

**How will we utilize it?**

- **CI** involves tracking changesith **Git/GitHub**, building & testing in **AWS Codebuild**, and ensuring the application code is error-free & ready for deployment.

- **CD** is handled by **AWS CodePipeline** and **AWS CodeDeploy**. The AWS CodePipeline orchestrates the flow, while AWS CodeDeploy deploys the application to EC2 instances, where Apache serves it to users.

# [What Are GitHub Actions?](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49663103#overview)

They're like robots that do tasks for you automatically when something happens in your code.

They can:
- test your code
- deploy your website or app
- run security checks
- send alerts or messages
- ... and more!

# [What is YAML?](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49663163#overview)

**YAML** is a **human friendly data serialization language** for all programming languages.

Provides a **simple way to write structured data** that's easy for both humans & computers to read

## How To Define a YAML Dictionary?

key / value pairs are separated by `:`

```yaml
name: John Smith
age: 30
job: Software Engineer
```

## How to Define a List in YAML?

A **list** is a group of values that can be stored under a single key in a dictionary

```yaml
- John Smith
- 30
- Software Engineer
```

## Combining Lists & Dictionaries

Can store a list of values under a key or have a list of dictionaries.

```yaml
name: John Smith
age: 30
job:
  title: Software Engineer
  description:  Problem solving with code
  books:
    - 20 ways to solve a coding bug
    - The complete software engineers handbook
    - clean and practical code
```

# [Create a Workflow to Automate Terraform Plan & Apply](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49771269#overview)

Need to ensure we create the correct directory structure.

In the main Django project folder, create a new `.github` folder with it's own `workflows` folder, which is what GitHub actions works with.

Now we need to set this all up for Terraform.

```yaml
name: Terraform workflow
```

This is a name for our workflow.

```yaml
on:
  push:
    branches:
      - main
```

This is the trigger - on pushes to main.

```yaml
jobs:
  terraform:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.11.4

      - name: Set up AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-2

      - name: Terraform Init
        run: terraform init

      - name: Terraform Plan
        run: terraform plan
        env:
          TF_VAR_RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
          TF_VAR_RENDER_OWNER_ID: ${{ secrets.RENDER_OWNER_ID }}
          TF_VAR_GHCR_USERNAME: ${{ secrets.GHCR_USERNAME }}
          TF_VAR_GHCR_PAT: ${{ secrets.GHCR_PAT }}
          TF_VAR_DATABASE_NAME: ${{ secrets.DATABASE_NAME }}
          TF_VAR_DATABASE_USER: ${{ secrets.DATABASE_USER }}
          TF_VAR_SECRET_KEY: ${{ secrets.SECRET_KEY }}

      - name: Wait for Approval
        uses: trstringer/manual-approval@v1.9.1
        with:
          approvers: {{ secrets.GHCR_USERNAME }}
          minimum-approvals: 1
          secret: ${{ secrets.GITHUB_TOKEN }} # - Behind the scenes temporary token generated

      - name: Terraform Apply
        run: terraform apply
        env:
          TF_VAR_RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
          TF_VAR_RENDER_OWNER_ID: ${{ secrets.RENDER_OWNER_ID }}
          TF_VAR_GHCR_USERNAME: ${{ secrets.GHCR_USERNAME }}
          TF_VAR_GHCR_PAT: ${{ secrets.GHCR_PAT }}
          TF_VAR_DATABASE_NAME: ${{ secrets.DATABASE_NAME }}
          TF_VAR_DATABASE_USER: ${{ secrets.DATABASE_USER }}
          TF_VAR_SECRET_KEY: ${{ secrets.SECRET_KEY }}
```

This section is the jobs that will be run. It will run on `ubuntu-latest` image (where our code will be run) and perform some series of steps. These steps may have the following pieces:

- `name`:  label of step
- `uses`:  identifies what GitHub action (reusable script or mini program that does a specific job in your workflow - pre-built tools you build into your automation pipeline) is being used
- `with`:  variables / inputs to use

To refer to a secret, you will use:  `${{ secrets.SOME_KEY }}`

Note that the `TF_VAR_` of the terraform vars allows Terraform to read from teh `main.tf` file & ensure it utilizes the correct ENV vars in the correct manner. It will take the GitHub secrets and ensure they are applied to the file. --- In other words, the whole section with `TF_VAR_` items are basically the `secrets.tfvars` file.

Here are the following steps:

1. CI:  checkout code to be run
2. CI:  set up Terraform & it's given version
3. CI:  set up AWS creds
4. CI:  initialize Terraform
5. CI:  run terraform plan
6. CD:  hold off until approved
7. CD:  apply terraform actions (where infra will be upgraded as written in `main.tf` file)

# [Terraform Workflow (Deep Dive)](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49924603#overview)

Emphsaied the AWS credentials from the `terraform.yaml` file.

The `Terraform Init` step will prepare Terraform to work by setting up it's backend & downloading providers. Must be run each time - mandatory. It won't initialize from scratch - will refer to `main.tf` file when it then comunicates with teh planning stage.

# [Create Workflow to Run Tests & Deploy App Automatically](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49771271#overview)

This is done on our application itself - not on our cloud infrastructure like with Terraform.

Will need the `application.yaml` file in the `.github/workflows` folder.

```yaml
name: Application workflow

on:
  workflow_run:
    workflows: ["Terraform workflow"]
    types:
      - completed
```

On workflow run, if `Terraform workflow` is completed do something ... Or we're only running this workflow after that workflow has completed.

```yaml
jobs:
  test:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    runs-on: ubuntu-latest
    env:
      SECRET_KEY: ${{ secrets.SECRET_KEY }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5.5.0
        with:
          python-version: '3.13'

      - name: Install dependencies
        run: |
          python -m venv venv
          source venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt

      - name: Check Django version
        run: |
          source venv/bin/activate
          python -m django --version

      - name: Collect static files
        run: |
          source venv/bin/activate
          python manage.py collectstatic --noinput

      - name: Run Django tests
        run: |
          source venv/bin/activate
          python manage.py test crm

      - name: Format code with Black
        run: |
          source venv/bin/activate
          black .

      - name: Linting with Ruff
        run: |
          source venv/bin/activate
          ruff check
```

This section above is for the testing phase. It is CI for our app.

```yaml

  deploy:
    runs-on: ubuntu-latest
    needs: test  # Only runs if the 'test' job succeeds

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5.5.0
        with:
          python-version: '3.13'

      - name: Install dependencies
        run: |
          python -m venv venv
          source venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3.4.0
        with:
          registry: ghcr.io
          username: ${{ secrets.GHCR_USERNAME }}
          password: ${{ secrets.GHCR_PAT }}

      - name: Build Docker image
        run: |
          docker build -t ghcr.io/devopscoder951/app-image .

      - name: Push Docker image
        run: |
          docker push ghcr.io/devopscoder951/app-image

      - name: Re-deploy your application on Render with a deploy hook
        run: |
          echo "Initialising deploy hook..."
          curl -X POST "${{ secrets.DEPLOY_HOOK_KEY }}"
```

The above is the final deploy stage. It is CD for our app.

This will only run if the `test` job was successful.

# Git Installation & Setup

https://git-scm.com/

# Ignoring Files for Git Ignore

Ensure the following are added from DockerIgnore:
```
.env
staticfiles/

main.tf
secrets.tfvars
.terraform/
.terraform.lock.hcl
*.tfstate
*.tfstate.*
```

# Create Private GitHub Repo

He outlined creating a private GitHub repo.

# [Assign Necessary Workflow Permissions](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49924615#overview)

Go to repo settings > actions > general > workflow permissions.

Choose default permissions granted to GitHub token when running workflos in repo.

Choose read/write permissions - requierd because we have an item that waits for approval. Also how the temporary GH token is made.

# [Define GitHub Secrets for Workflows](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49924617#overview)

In your repo, go to: `Settings > Secrets and variables > Actions`

This is where you will define the secrets to work with GH Actions.

The video only showed repo secrets, but going there now shows environment secrets as well. Learn more about them [here](https://docs.github.com/en/actions/how-tos/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables).

Add your secrets from your secrets file.

The variable names / labels after `{{ secret.VAR_NAME }}` must match what you put in this section of the repo.

We don't use the DB in the workflow, but for good measure should put the secrets in.

This should also include your AWS items that were not in the terraform vars file, but the terraform & application YAML files.

The keys:
- `RENDER_API_KEY`
- `RENDER_OWNER_ID`
- `GHCR_USERNAME`
- `GHCR_PAT`
- `DB_NAME`
- `DB_USER`
- `SECRET_KEY`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `DEPLOY_HOOK_KEY`

The deploy hook key is the API URL you get from Render's settings under **Deploy Hook**.

# [Terraform Workflow Adjustment](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49924623#overview)

Go to the `Wait for Approval` step in the `terraform.yaml` file. Temporarily comment it out to ensure you can easily set up your CICD pipeline automatically for infrastructure and application code.

```yaml
      - name: Wait for Approval
        uses: trstringer/manual-approval@v1.9.1
        with:
          approvers: {{ secrets.GHCR_USERNAME }}
          minimum-approvals: 1
          secret: ${{ secrets.GITHUB_TOKEN }}
```

Add an auto approve flag on the `terraform apply` stage by adding `-auto-approve`:

```yaml
      - name: Terraform Apply
        run: terraform apply -auto-approve
        env:
          TF_VAR_RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
          TF_VAR_RENDER_OWNER_ID: ${{ secrets.RENDER_OWNER_ID }}
          TF_VAR_GHCR_USERNAME: ${{ secrets.GHCR_USERNAME }}
          TF_VAR_GHCR_PAT: ${{ secrets.GHCR_PAT }}
          TF_VAR_DATABASE_NAME: ${{ secrets.DATABASE_NAME }}
          TF_VAR_DATABASE_USER: ${{ secrets.DATABASE_USER }}
          TF_VAR_SECRET_KEY: ${{ secrets.SECRET_KEY }}
```

# [Setup a Lifecycle Rule in Terraform](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49924629#overview)

Focus on adjusting Terraform configuration to ensure our ENV vars have been set & not interfered with or updated in any way.

In the `main.tf` file, go to the `render_web_service` you'll see that `env_vars`  were only defined with the `secret_key`.

If we went ahead and run `terraform init` and `terraform plan` and `terrform apply` it's going to remove what's in Render (env vars for our DB) so coincide with what is in this file.

To prevent that and ensure Terraform only deals with infrastructure side (e.g. resources, web service, postgres DB, creds) we would set up a lifecycle rule within the web service.

Below where env var is defined, we want to ignore changes on them. This will take into account the ENV vars we defined with the postgres DB.

```
resource "render_web_service" "WebApp1" {
  
  name   = "my-django-app"
  plan   = "starter"
  region = "oregon"

   runtime_source = {
    image = {
      image_url = "ghcr.io/prosperousheart/app-image"
      tag = "latest"  
      registry_credential_id = render_registry_credential.ghcr_credential.id
    }
  }

  env_vars = {
    SECRET_KEY = {value = var.SECRET_KEY}
  }

  lifecycle  {
    ignore_changes = {
      env_vars
    }
  }

}
```

# [Configure DBs for DEV and PROD](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49925637#overview)

Focus on ensuring our DB is working fine in terms of running tests & ensure working perfectly fine in regards from managing the expectations with switching from a PROD DB to a DEV DB and vice versa.

When we run our checks in the CI phase, there is going to be a chance that we run into an error in terms of our postgres DB.

We won't have our `.env` file available so we won't be able to utilize our postgres DB in any way or even connect to it.

What we need to do in the testing phase, we would need to ensure that we at least have a default value set for our postgres DB.

To ensure that the SQLite DB just takes form in light of something that is workingfine and not breaking.

So to resolve the issue of the `.env` file, go to the main project's `settings.py` file ...

1. uncomment out the SQLite DB and leave postgres as is

2. switch to a postgres DB if the name is avaialble ... ensure the database name is a check

    - above the postgres DB add:

    ```python
    DB_NAME = env("DB_NAME", default=None)
    ```

    - add if statement to the postgres section:

    ```python
    if DB_NAME:
      DATABASES = {
          "default": {
              "ENGINE": "django.db.backends.postgresql",
              "NAME": env("DB_NAME", default="my_database_2mtk"),
              "USER": env("DB_USER"),
              "PASSWORD": env("DB_PASSWORD"),
              "HOST": env("DB_HOST"),
              "PORT": env("DB_PORT"),
          }
      }
    ```

    - if you haven't already, set up default values for the fields to ensure nothing breaks & everything is clean in terms of the CI phase:

    ```python
        DATABASES = {
          "default": {
              "ENGINE": "django.db.backends.postgresql",
              "NAME": env("DB_NAME", default="my_database_2mtk"),
              "USER": env("DB_USER", default=''),
              "PASSWORD": env("DB_PASSWORD", default=''),
              "HOST": env("DB_HOST", default=''),
              "PORT": env("DB_PORT", default=''),
          }
       }
    ```

# [Push to Private Repo](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49784297#overview)

