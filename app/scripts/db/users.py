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

def get_hash(email):
    response = table.get_item(
        Key = {
            'email': email
        },
        AttributesToGet = ['password', 'salt']
    )
    return response['Item']

class User(UserMixin):
    '''
    User class
    '''
    def __init__(self, uuid, email, studies, password, salt):
        self.uuid = uuid
        self.email = email
        self.studies = studies
        self.password = password
        self.salt = salt
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False

    @staticmethod
    def get(uuid):
        try:
            response = table.get_item(
                Key = {'uuid': uuid},
                AttributesToGet = ['uuid', 'email', 'studies']
                )
            user_data = response['Item']
            if user_data:
                return User(uuid = user_data['uuid'],
                            email = user_data['email'],
                            studies = user_data['studies'])
            else:
                return None
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None

    @staticmethod
    def create(email, password):
        if check_email_exists(email) > 0:
            return 'Email in use'
        else:
            hashed = hash_encode(password)
            uuid = email + datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            uuid = hash_encode(uuid)[0]
            new_user = {'uuid': uuid, 
                        'email': email, 
                        'password': hashed[0], 
                        'salt': hashed[1], 
                        'verified': False,
                        'studies': []}
            try:
                table.put_item(
                    Item = new_user
                )
                return 'Check email to complete registration.' 
            except ClientError as e:
                print(e.response['Error']['Message'])
                return None

    @staticmethod
    def remove(email, password):
        if check_email_exists(email) < 1:
            return 'User does not exist'
        credentials = get_hash(email)
        if hash_encode(password, credentials['salt'].__str__())[0] != credentials['password']:
            return 'Incorrect password'
        else:
            table.delete_item(
                Key = {
                    'email': email
                }
            )

