from boto3 import Session
from config import config
from werkzeug.utils import secure_filename

session = Session(aws_access_key_id = config.ACCESS_KEY_ID,
                  aws_secret_access_key = config.SECRET_ACCESS_KEY,
                  region_name = config.REGION_NAME)
s3 = session.resource('s3')

def upload_file():
    pass