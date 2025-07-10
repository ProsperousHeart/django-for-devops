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