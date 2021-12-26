# Prefect ECS Agent for CoinMarketCap Scrapper
The repository creates a Prefect flows and registers it to Prefect Project. The prefect flow is an ELT process with:

  1. **Extract task:** Here the requests and beautifulSoup libraries are used to scrap relevant data from webpage.
  2. **Transform task:** This tasks transforms currency unit from USD to AUD.
  3. **Load task:** This task saves the transformed dataset into S3 container.

The three of these abovementioned functions are processed into a flow, in the file prefect-ecs.py. 

Further a Dockerfile is created that that could register a flow, set up and run Prefect ECS Agent. The ECR Image can be found [here](https://gallery.ecr.aws/s0c5i6w0/prefect-service-image)

# Deployment Procedure

The deployment procedure consists of following steps:
  1. Updating system files and installing github
  2. Cloning repository
  3. Adding credentials to Dockerfile
  4. Installing Docker
  5. Building Docker Image
  6. Taging and Pushing Image to ECR Public Repository
 
Lets start

## 1. Updating system files and installing github

Run following commands
```
sudo apt update
sudo apt install git
```
## 2. Cloning repository

Run the following code:
```
git clone https://github.com/usamatrq94/Prefect-ECSAgent-Deploy.git
cd /Prefect-ECSAgent-Deploy
```
## 3. Adding credentials to Dockerfile

The Dockerfile needs some credentials. Please add Prefect access token and AWS ACCESS_KEY_ID and SECRET_ACCESS_KEY.
```
nano Dockerfile
```
## 4. Installing Docker

Run the following code line by line to download docker from official repository
```
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add –
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu  $(lsb_release -cs)  stable" 
sudo apt-get update
sudo apt-get install docker-ce
```
With this done, we need to manage permissions for our user. This will help avoid typing sudo whenever you run the docker command. We can do that using following code.
```
sudo usermod -a -G docker ${USER}
```
## 5. Building Docker Image

Building Docker Image
```
docker build -t prefect-service-image .
```
## 6. Taging and Pushing Image to ECR Public Repository

After the build completes, tag your image so you can push the image to this repository:
```
docker tag prefect-service-image:latest public.ecr.aws/s0c5i6w0/prefect-service-image:latest
```
Run the following command to push this image to your newly created AWS repository:
```
docker push public.ecr.aws/s0c5i6w0/prefect-service-image:latest
```



