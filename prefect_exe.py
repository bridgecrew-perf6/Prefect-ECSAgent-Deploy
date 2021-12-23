from prefect.storage import S3
from prefect.run_configs import ECSRun
from prefect import task, Flow
import extract
import transform
import load

TASK_ARN = "arn:aws:iam::776883799019:role/ECSTaskS3Role"
RUN_CONFIG = ECSRun(labels=['s3-flow-storage'],
                    task_role_arn=TASK_ARN,
                    image='anisienia/prefect-pydata',
                    memory=512, cpu=256)
STORAGE = S3(bucket='prefect-bucket-2021')

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

with Flow("s3_pandas", storage=STORAGE,
        run_config=RUN_CONFIG) as flow:
    scrap_data = extract_task()
    aud_data = transform_task(scrap_data)
    load_task(aud_data)

flow.register(project_name="04-fargate")
