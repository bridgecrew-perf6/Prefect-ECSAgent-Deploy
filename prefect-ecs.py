import extract
import transform
import load
import prefect
from prefect import Flow, storage, task
from prefect.run_configs import ECSRun
from datetime import timedelta, datetime
from prefect.schedules import IntervalSchedule
from prefect.storage import S3

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
    
schedule = IntervalSchedule(
        start_date=datetime.utcnow() + timedelta(seconds=1), interval = timedelta(minutes=5))

run_config = ECSRun(
        image="public.ecr.aws/s0c5i6w0/prefect-task-image:latest",
        task_role_arn="arn:aws:iam::776883799019:role/ecsTaskExecutionRole",
        labels=['simple-prefect-task']
        )

storage = S3(bucket="prefect-bucket-2021")

with Flow("Scrap-Top-Gainers", schedule=schedule, run_config=run_config, storage=storage) as flow:
    logger = prefect.context.get("logger")
    logger.info("Scrapping Process Started")
    scrap_data = extract_task()

    logger.info("Data scrapped successfully!, coverting to AUD.")
    aud_data = transform_task(scrap_data)

    logger.info("Coverted to AUD successfully, loading data to S3")
    load_task(aud_data)
    logger.info("Data load to S3 - Top Crypto Gainers Bucket - succesful!")


flow.register(project_name="ECS-Fargate")

#client = Client()
#client.create_flow_run(version_group_id = "b7d03774-17ff-45aa-8ed5-18ca4221790d")
#prefect agent ecs start --cluster  my-prefect --label simple-prefect-service-2 --label DESKTOP-6DKKJAV --name ECS-Fargate