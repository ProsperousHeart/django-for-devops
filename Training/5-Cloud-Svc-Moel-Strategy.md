

# Cloud Service Models & Strategy

## Service Models

1. **IaaS (Infrastructure as a Service)**:  provides VMs, storage, & networking allowing users to manage their own software while the cloud provider handles the hardware (e.g.:  AWS EC2)

![IaaS](/IMGs/section-05/5-cloud-service-IaaS.png)

2. **PaaS (Platform as a Service)**:  offers a pre-configured platform for developing, running, & managing applications without worrying about underlying infrastructure (e.g.: Render, Heroku, Railway, AWS Elastic Beanstalk) ... simplest way to deploy your app!

![PaaS](/IMGs/section-05/5-cloud-service-PaaS.png)

3. **IaC (Infrastructure as Code)**:  automates cloud resource provisioning & management using code

![IaC](/IMGs/section-05/5-cloud-service-IaC.png)

## Use Case 1:  PaaS

![use case 1](/IMGs/section-05/5-cloud-service-use-case-1.png)

## Use Case 2:  IaC

**Terraform** is an infrastructure as code tool. We'll utilize it so we can write the necessary code & communicate with render, so we can setup the resources to be provisioned based on the code we write with Terraform.

![use case 2](/IMGs/section-05/5-cloud-service-use-case-2.png)