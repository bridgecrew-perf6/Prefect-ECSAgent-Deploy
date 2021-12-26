import extract, transform, load
import prefect
from prefect import Flow, storage, task
from prefect.run_configs import ECSRun
from datetime import timedelta, datetime
from prefect.schedules import IntervalSchedule
from prefect.storage import S3

# below are prefect decored tasks, which are just calling functions from
# extract, transform and load python scripts

@task
def extract_task():
    top_gainers = extract.top_gainers_today()
    return top_gainers

@task
def transform_task(dataframe):
    dataframe = transform.transform_data(dataframe)
    return dataframe

@task
def load_task(dataframe):
    load.upload_to_s3(dataframe)
    
# setting up a schedule to be able to execute this flow everyday
schedule = IntervalSchedule(
        start_date=datetime.utcnow() + timedelta(seconds=1), interval = timedelta(days=1))

# setting run configuration for ECS Agent, it has three parts: image, task_role and labels
# image: This the image to be used for ECS Task i-e the docker container running the flow on ECS-fargate
# the image is fetched from ECR public repository and dockerfile for this image can be found at: 
# https://github.com/usamatrq94/crypto_scrapper/blob/main/Dockerfile
# task_role_arn: Needs a role, attached to ECS to allow ECS to call AWS services on your behalf
# task_role needs permissions to read/write from S3, read/write to ECR and
# AmazonECSTaskExecutionRolePolicy to write logs to CloudWatch
# lables: Each flow and agent has labels attached to them and only agents having all labels on the flow
# are able to execute that flow.
run_config = ECSRun(
        image="public.ecr.aws/s0c5i6w0/prefect-task-image:latest",
        task_role_arn="arn:aws:iam::776883799019:role/ecsTaskExecutionRole",
        labels=['Alb-Fargate-Flow']
        )

# setting flow storage to S3 bucket. Whenever flow and polling agent are registered on different containers,
# prefect requires its flow metadata to be saved externally like S3.
storage = S3(bucket="prefect-bucket-2021")

# creating a flow with above parameters and specifying pattern
with Flow("Scrap-Top-Gainers", schedule=schedule, run_config=run_config, storage=storage) as flow:
    # Extract Task
    logger = prefect.context.get("logger")
    logger.info("Scrapping Process Started")
    scrap_data = extract_task()
    
    # Transform Task
    logger.info("Data scrapped successfully!, coverting to AUD.")
    aud_data = transform_task(scrap_data)

    # Load Task
    logger.info("Coverted to AUD successfully, loading data to S3")
    load_task(aud_data)
    logger.info("Data load to S3 - Top Crypto Gainers Bucket - succesful!")

# registering your flow to prefect project
flow.register(project_name="Alb-Fargate")

#client = Client()
#client.create_flow_run(version_group_id = "b7d03774-17ff-45aa-8ed5-18ca4221790d")
#prefect agent ecs start --cluster  my-prefect --label simple-prefect-service-2 --label DESKTOP-6DKKJAV --name ECS-Fargate
