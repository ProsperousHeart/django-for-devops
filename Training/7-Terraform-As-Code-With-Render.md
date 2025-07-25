[Table of Contents](/README.md)

# IaC with Render & Terraform

## [What is Terraform?](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49343125#overview)

**Terraform** is a tool that helps you set upa nd manage your cloud infrastructure (i.e.: servers, DBs, networks) **using simple code** instead of clicking around in a dashboard (i.e. what we did earlier with PaaS)

Lets you describe what your cloud setup should look like in files, then automatically builds everything to match that description.

## [Installing & Setting Up - WIN](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49343135#overview)

Download from [their site](https://developer.hashicorp.com/terraform) - likely to install AMD64. Extract it to wherever you want it to be. (He put on desktop then moves it to `Program Files`.)

Ensure we set the Terraform folder up within our program files.

Edit environment variables so that in **system variables > path** to add the directory the Terraform application is in:  `C:\Program Files\Terraform`

Suggested to restart your PC to ensure run variables are loaded properly.

You can confirm if set up properly by going to CMD and typing:  `terraform --version`

Just typing `terraform` will provide commands you can use.

## [Add Render Payment Method & Analyze Costs](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49601911#overview)

If we want to utilize IaC and automatically create our IaC with Terraform, we need to utilize a starter instance when working with Terraform and IaC. Our DB will be free, so no worries there. (i.e. only the web service)

[Render pricing](https://render.com/pricing) - check out the [compute section](https://render.com/pricing#compute). If you don't use the whole month, it won't cost you. It only costs when using the whole month. (He created them for only a couple hours and wasn't charged.)

Manually you can set it all up for free. But when using IaC (likely a security measure) onyl with web services you have to use a starter instance & card on Render.

## [Obtain Render API Key & Owner ID](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49601903#overview)

This will allow us to communicate with Render, create our infrastructure, & requests to Render for retrieving our own ID.

Go to your **Account Settings** then go to your **API Keys** section.

Create an API key form here for this project. He called it:  **RenderAPIKey**

The response is only visible to you once. You can always revoke a key if it gets compromised.

Need to make GET request so we can obtain our owner ID. In your terminal:

```terminal
curl -X GET -H "Accept: application/json -H "Authorization: Bearer RENDER_API_KEY" https://api.render.com/v1/owners
```

This is the header that will tell our server (Render) that we want the response returned in JSON format.

We self authorize with the API key

Render API endpoint is at the end.

![GET owner via CMD CURL](/IMGs/section-07/7-render-GET-owner.png)

Learn more about Render API [here](https://api-docs.render.com/reference/introduction).

## [How to define Cloud Resources with Terraform in Code?](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49601637#overview)

What is the [Terraform registry](https://registry.terraform.io/?product_intent=terraform)? It has a variety of providers available it is compatible with. We'll use **[render-oss](https://registry.terraform.io/providers/render-oss/render/latest)** - the IaC layout or blueprint for Terraform. At the time I went through this training, it was version:  **1.7.0**

When you go to the [documentation](https://registry.terraform.io/providers/render-oss/render/latest/docs) you'll see it's the official Render provider ^ we need to provide some starting up information (e.g.:  API key, owner ID, etc).

The resources drop down on the left has other things you may be interested in utilizing. (e.g.:  setting upa  web service)

## Build Cloud Infra in Terraform

### [Part 1](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49601949#overview)

Focused on building cloud resources with Terraform in code.

He gave a basic template to put intot he main project folder. Explanations:

```
terraform {
  required_providers {
    render = {
      source  = "render-oss/render"
      version = "1.7.0"
    }
  }
}
```

The above block sets some of the basic setup rules for Terraform:

   - The **required_providers** lists all of the Terraform providers we will use.

   - The **source** is like teh official name in the registry.

   - The **version** is what we want to use of the provider to keep things stable and predictable.

```
provider "render" {
  api_key  = ""
  owner_id = ""
}
```

The provider section needs to have data filled in.

Below is where we are defining our resource(s):
- [render_registry_credential](https://registry.terraform.io/providers/render-oss/render/latest/docs/resources/registry_credential)
- [render_web_service](https://registry.terraform.io/providers/render-oss/render/latest/docs/resources/web_service)

The final element in the calls after the service name are names you give them - acts as a label for the resource created.

```
# Define Render Registry Credential for GitHub Container Registry (GHCR)

resource "render_registry_credential" "ghcr_credential" {
  name = "ghcr-credential"
  registry = "GITHUB"
  username = ""
  auth_token = ""  
}
```

The **name** refers to the registry credential within Render so it can be whatever you want.

The **registry** defines where your Docker image currently exists. Might use **ECR** for AWS or something similar.

```
# Define the Render Web Service

resource "render_web_service" "WebApp1" {
  
  name   = "my-django-app"
  plan   = "starter"
  region = "oregon"

   runtime_source = {
    image = {
      image_url = "ghcr.io/<GitHub username>/app-image"
      tag = "latest"  
      registry_credential_id = render_registry_credential.ghcr_credential.id
    }
  }


}
```

The 3rd part of the call (e.g.:  `"WebApp1"`) is only used behind the scenes for setting up resources in Terraform. (like a label)

The **name** field will be the name of the web service - call it whatever you want.

The **plan** needs to be **starter**.

You'll need to update the **runtime_source** section as this is where it will pull the image from. It defines how our runtime ENV is sourced.

   - the **image_url** username must be in lower case
   - **tag** is essentially the version tag for the Docker image
   - the **registry_credential_id** refers to something made earlier in the file according to it's `.id` attribute (essentially the ID of the registry credentials we use to authenticate against the GHCR)

### Part 2

Relates to [render_postgres](https://registry.terraform.io/providers/render-oss/render/latest/docs/resources/postgres).

```
resource "render_postgres" "Database1" {

    name = "ProductionDatabase1"
    plan = "free"       
    region = "oregon"      
    version = "16"

    database_name = ""
    database_user = ""

    high_availability_enabled = false  # Disabled high availability for simplicity

  }
```

The **name** is what is used to ID and manage the DB instance within Render. (label)

The **database_name** (e.g.:  MyDatabase) and **database_user** (e.g.: DemoUser) is what Render provides. (actual DB name)

## [Configure ENV Variables for Terraform](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49601655#overview)

Create the following file in the main project folder:  `secrets.tfvars`

Add the following:
- Render API Key
- render ownerID
- GHCR username & PAT
- DB name and user
- secret Django key

In the TF vars file, find space to define the ENV variables - he suggested above the provider section.

Form:  `variable "KEY_NAME_HERE" {additional info}`

The **additional info** relates to additional settings.

![initializing TF vars](/IMGs/section-07/7-TF-vars.png)

Replace hard coded values in the `main.tf` file by calling:  `var.VAR_NAME`

Web service wil be a little different - within it's code blocks is where we're define variables.

![configure web service](/IMGs/section-07/7-vars-for-web-svc.png)

## [Compare Distinction Between PaaS and IaC Pre-Deployment](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49601667#overview)

This just covered how this applied to manually setting up within Render like before.

## [Re-Dockerize & Configure PROD Docker Image](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49546027#overview)

We'll leave the sqlite for now.

Need to add the secrets files to `.gitignore` and `dockerignore` files.

```
main.tf
secrets.tfvars
```

Time to build the Docker image!

```
docker build -t ghcr.io/prosperousheart/app-image .
docker push ghcr.io/prosperousheart/app-image
```

## [Best Practices for DB Value Naming](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49731023#overview)

Beest practices and managing expectations with naming conventions.

May differ with Render, but when it comes to IaaS there is a convention to follow.

`MyDatabase` --> `my_database`

`DemoUser` --> `my_database_user`

## [Create Infra And Deploy App with IaC](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49601691#overview)

In CMD within main project folder, send:  `terraform init`

This will initialize the Terraform working directory & install all required providers. Will also prep the environment for you.

**NOTE:**  Be sure you only have 1 Terraform file that is making certain commands. Otherwise it will think there are duplicates and fail to initiate.

![TF init outcome](/IMGs/section-07/7-Terraform-init.png)

Send `terraform plan -var-file="secrets.tfvars"` to continue setup. This will review our code in terms of our `main.tf` file as to what infra we want to setup. It will also show what changes will be made without actually applying it. (Gives you a chance to review your code!)

Recommended to also refer to your ENV var file to ensure that Terraform has ability to read from these values.

![TF plan](/IMGs/section-07/7-TF-plan.png)

`terraform apply -var-file="secrets.tfvars"`

![TF apply](/IMGs/section-07/7-complete-IaC-TF-apply.png)

Once you say "yes" it will create your infra.

You can see them being built in real time on Render:

![built in RT on render](/IMGs/section-07/7-RT-built-on-render.png)

## [Configure PostgreSQL DB And Deployment Settings](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49731039#overview)

This will be focused on connecting our Postgres DB & makign final deployment configurations within the `settings.py` file of main project.

Go to the settings of your new Render database & update the `settings.py` file mockup, then:
- comment out the SQLite confi
- uncomment the POSTGRES config

![tweaked postgres configs](/IMGs/section-07/7-tweaked-postgres-db-config.png)

- update `.env` file

Generally speaking when you are working with postgres DB and want to create a superuser & make your migrations, you usually use an external DB URL & then connect to it.

We plan to make migratiosn diretly in Render shell so don't need external URL.

Need to make deployment configurations, so need to:

- update allowed hosts to have domain name that is given by Render's web service (local IP is being left from prior time - not in video)

    ![allowed hosts update](/IMGs/section-07/7-allowed_hosts_update.png)

- add back CSRF trusted origin using the allowed host from Render (to ensure we allow POST requests on our domain)

    ![update CSRF](/IMGs/section-07/7-update-CSRF.png)

- double check that `DEBUG` is set to `False`

- ignore Terraform directory that was created (in both Docker ignore and gitignore) as well as the lock file & `.tfstate` file

    We want to ignore teh TF folder from Docker because no need to include (TF is for infra building, nothing to do with actual app that Docker is used for)

    ```
    main.tf
    secrets.tfvars
    .terraform/
    .terraform.lock.hcl
    *.tfstate
    *.tfstate.*
    ```

Clean up old images for Docker then run:  `docker system prune`

Now we can revbuild docker image:  `docker build -t ghcr.io/prosperousheart/app-image .`

Push to GHCR:  `docker push ghcr.io/prosperousheart/app-image`

Can confirm push by going to your packages.

The web service does not automatically rebuild the deployment. Using CICD with GitHub, we will be able to automatically set this up for automated updates.

## [Assign DB ENV Vars in Render](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49731139#overview)

Now need to configure the DB creds in terms of ENV vars.

Goto DB instance.

Go to the web service environment section. Update as neeed and hti the "Save & Deploy" button.

When you update your ENV vars, it looks for the latest & redepolys your service.

Go to the SHELL section of your web service. This allos you to essentially SSH into your application. The Docker directory we set up is called `app`:

![shell init output](/IMGs/section-07/7-shell-init-output.png)

We can access the application, make a migration, create superuser, etc.

## [Utilize the Render Shell](http://udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49731141#overview)

If you try to run `python manage.py migrate` there would be nothing because the `entrypoint.sh` file already has this.

Only thing you cannot go around or skip ahead on is creating the **superuser**:  `python manage.py createsuperuser`

Test POST call and admin site.

## [Call Deploy Hook to Handle Re-Deployments](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49731151#overview)

Simple change - don't need to redeploy Docker.

In `static` directory, change color of heading to blue. Tweak the index page template.

Build & push docker image:

```
docker build -t ghcr.io/prosperousheart/app-image .
docker push ghcr.io/prosperousheart/app-image
```

Nothing will have happened. For your web service, go to **Settings** and locate the `Deploy hook` section. Copy the private hook URL.

On local machine, run the following in command prompt:  `curl -X POST "API_URL_DEPLOY_HOOK_HERE"`

![web hook local setup](/IMGs/section-07/7-create-web-hook.png)

Can see the events that the hook kicked off a redeploy:

![web hook triggers redeploy](/IMGs/section-07/7-redeploy-triggered.png)

Test redeployment by refreshing the page of your app.

## [Compare Distinction Between PaaS and IaC Post-Deployment](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49731161#overview)

Considering the `main.tf` file ...

For `WebApp1` (the web service) the `registry_credential_id` ...

When you go to your Render dashboard then your web service, settings -- can see the GHCR credential as well as the image URL.

## [Exploring Purpose of Additional TF Files](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49602043#overview)

1. `.terraform` folder - stores all internal files & downlodaed plugins that TF needs in order to run

2. `.terraform.lock.hcl` - locks versions of providers we have utilized to ensure we always have a consistent setup across different machines

3. `terraform.tfstate` - keeps track of infra we've created so TF knows what exists