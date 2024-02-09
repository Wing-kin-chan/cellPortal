'''
Functions to get, managing items (users) when registering or deleting accounts, 
check user credentials for logging in.
'''

from boto3.session import Session
import bcrypt
from config import config

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

def new_user(email, password):
    if check_email_exists(email) > 0:
        return 'Email in use'
    else:
        hashed = hash_encode(password)
        new_user = {'email': email, 'password': hashed[0], 'salt': hashed[1]}
    table.put_item(
        Item = new_user
    )
    return 'Check email to complete registration.'

def login(email, password):
    if check_email_exists(email) == 0:
        return 'Email does not exist'
    credentials = get_hash(email)
    if hash_encode(password, credentials['salt'].__str__())[0] != credentials['password']:
        return 'Incorrect password'
    else:
        return 'Logged in'
        

def delete_user(email, password):
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

