FROM prefecthq/prefect:latest-python3.7
 
RUN apt-get update && apt-get install -y --no-install-recommends \
sudo \
libcurl4-gnutls-dev \
libcairo2-dev \
libxt-dev \
libssl-dev \
libssh2-1-dev \
libxml2-dev \
  && rm -rf /var/lib/apt/lists/*

RUN pip install "prefect[aws,viz]"

RUN prefect backend cloud

RUN prefect auth login --key **prefect-cloud-tocken**

RUN prefect create project "ECS-Task-Container"

RUN mkdir Task-Container

COPY * ./Task-Container/

WORKDIR /Task-Container

RUN pip install -r requirements.txt

RUN python prefect-ecs.py
