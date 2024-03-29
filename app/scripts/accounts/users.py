'''
Functions to get, managing items (users) when registering or deleting accounts, 
check user credentials for logging in.
'''

from boto3.session import Session
from botocore.exceptions import ClientError
import bcrypt
from config import config
from flask_login import UserMixin
from datetime import datetime


session = Session(aws_access_key_id = config.ACCESS_KEY_ID,
                  aws_secret_access_key = config.SECRET_ACCESS_KEY,
                  region_name = config.REGION_NAME)
table = session.resource('dynamodb').Table(config.USER_TABLE)


def hash_encode(input, salt = None):
    if not salt:
        salt = bcrypt.gensalt()
    encoded = bcrypt.hashpw(input.encode('utf8'), salt)
    out = encoded.decode('utf8')
    return out, salt

def check_email_exists(email: str):
    response = table.query(
        Select = 'COUNT',
        KeyConditionExpression = '#pk = :pk',
        ExpressionAttributeNames = {
            '#pk': 'email'
        },
        ExpressionAttributeValues = {
            ':pk': email
        },
    )
    return response['Count']

class User(UserMixin):
    '''
    User class
    '''
    def __init__(self, email: str, uuid: str, password: str, salt: bytes, isVerified: bool):
        self.email = email
        self.uuid = uuid
        self.password = password
        self.salt = salt
        self.isVerified = isVerified
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.email
        
    @staticmethod
    def get_user(email: str):
        try:
            response = table.get_item(
                Key = {'email': email}
                )
            user_data = response['Item']
            if user_data:
                return User(uuid = user_data['id'],
                            email = user_data['email'],
                            password = user_data['password'],
                            salt = user_data['salt'],
                            isVerified = user_data['isVerified'])
            else:
                return None
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None

    @staticmethod
    def create(email: str, password: str):
        if check_email_exists(email) > 0:
            return 'Email in use'
        else:
            hashed = hash_encode(password)
            id = email + datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            id = hash_encode(id)[0]
            new_user = {'id': id, 
                        'email': email, 
                        'password': hashed[0], 
                        'salt': hashed[1], 
                        'isVerified': False
                        }
            try:
                table.put_item(
                    Item = new_user
                )
                return 'Check email to complete registration.' 
            except ClientError as e:
                print(e.response['Error']['Message'])
                return None

    @staticmethod
    def verify(email: str):
        if check_email_exists(email) < 1:
            return 'User does not exist'
        else:
            try:
                table.update_item(
                    Key = {'email': email},
                    UpdateExpression = 'SET isVerified = :value',
                    ExpressionAttributeValues = {':value': True}
                )
            except ClientError as e:
                print(e.response['Error']['Message'])
                return None

    @staticmethod
    def remove(email: str):
        if check_email_exists(email) < 1:
            return 'User does not exist'
        try:
            table.delete_item(
                Key = {
                    'email': email
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None

