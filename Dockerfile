# git repository 
# https://github.com/usamatrq94/Prefect-ECSAgent-Deploy
# Fetch base Prefect Image for Python 3.7.12 
FROM prefecthq/prefect:latest-python3.7

# installing packages and updating system libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
   sudo \
   libcurl4-gnutls-dev \
   libcairo2-dev \
   libxt-dev \
   libssl-dev \
   libssh2-1-dev \
   libxml2-dev \
   && rm -rf /var/lib/apt/lists/*

# installing prefect AWS and Visualizations dependencies
RUN pip install "prefect[aws,viz]"

# configure Prefect to use the Prefect Cloud backend
RUN prefect backend cloud

# Authenticating Prefect Cloud Token
RUN prefect auth login --key **prefect-cloud-tocken**

# Setting AWS configure as envoirnment variables to access S3 to store flow metadata
# Access keys should be for appropriate IAM role with read and write permission to S3
ENV AWS_ACCESS_KEY_ID="your-access-key"
ENV AWS_SECRET_ACCESS_KEY="your-secret-key"
ENV AWS_DEFAULT_REGION="your-default-region"

# Create a new prefect project
RUN prefect create project "ECS-Task-Container"

# Create a new directory - Task-Container
RUN mkdir Task-Container

# Copy all python scripts to docker container folder - Task-Container
COPY * ./Task-Container/

# Set Task-Container as workind directory
WORKDIR /Task-Container

# Install all required dependencies
RUN pip install -r requirements.txt

# Creating a file to allow load.py to excess S3, redundant, should be done through env variables 
RUN echo "aws_keys={'access_key':AWS_ACCESS_KEY_ID,'secret_key':AWS_SECRET_ACCESS_KEY}" > CryptoBucketUser.py

# Register prefect flow
CMD ["python","prefect-ecs.py"]

# Start Prefect ECS Agent on Cluster: my-prefect
CMD ["prefect","agent","ecs","start","--cluster","arn:aws:ecs:ap-southeast-2:776883799019:cluster/my-prefect","--label", \
   "simple-prefect-task-2","--name","ECS-Task-Container"]
