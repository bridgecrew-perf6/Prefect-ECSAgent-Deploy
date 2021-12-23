import io
import boto3
from datetime import datetime
from CryptoBucketUser import aws_keys

# connecting to S3-client to excess s3 buckets
s3_client = boto3.client(
    's3',
    region_name='ap-southeast-2',
    aws_access_key_id=aws_keys['access_key'],
    aws_secret_access_key=aws_keys['secret_key']
)

# the function belows checks if the connection to S3 is successful or not
def get_status(response):
    result = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
    
    if result == 200:
        status = f"Upload Successful - {result}"
    else:
        status = f"Upload Unsuccessful - {result}" 
    return status

# the functions returns a datetime string of current time, to be used as filenames
def get_file_name():
    file_name = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    file_name = file_name.replace(" ", "-") + ".csv"
    return file_name
    
# the function uploads the transformed dataframe to S3
def upload_to_s3(data):
    with io.StringIO() as csv_buffer:
        data.to_csv(csv_buffer, index=False)
        
        key = "gainers/" + get_file_name()
        
        response = s3_client.put_object(
            Bucket='crypto-top-gainers', Key=key , Body=csv_buffer.getvalue()
        )
        status = get_status(response)
        print(status)
