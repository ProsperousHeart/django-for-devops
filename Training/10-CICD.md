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