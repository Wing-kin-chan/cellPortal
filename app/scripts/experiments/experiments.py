'''
Functions to search for, and manage experiments on the experiments table and storage server.
'''

from boto3 import Session
from botocore.exceptions import ClientError
from config import config
from dataclasses import dataclass

session = Session(aws_access_key_id = config.ACCESS_KEY_ID,
                  aws_secret_access_key = config.SECRET_ACCESS_KEY,
                  region_name = config.REGION_NAME)
table = session.resource('dynamodb').Table(config.EXPERIMENTS_TABLE)

@dataclass
class Experiment:
    '''
    Data class to hold experiment metadata
    '''

    def __init__(self, 
                 uuid: str, 
                 title: str, 
                 cells: int, 
                 assay: str, 
                 tissue: str, 
                 organism: str, 
                 celltypes: list,
                 s3: str,
                 tags: list):
        self.uuid = uuid
        self.title = title
        self.cells = cells
        self.assay = assay
        self.tissue = tissue
        self.organism = organism
        self.celltypes = celltypes
        self.s3 = s3
        self.tags = tags

    def __str__(self):
        return f'Owner UUID: {self.uuid} Title: {self.title} S3 Address: {self.s3}'

    def __repr__(self):
        print(f'''
            Experiment Database Entry  
            Owner UUID: {self.uuid}  
            Title: {self.title}  
            S3 Address: {self.s3}  
        ''')


    @staticmethod
    def record(self) -> None:
        '''Stores metadata of experiment in DynamoDB'''
        pass
    

    @staticmethod
    def erase(self) -> None:
        '''Removes metadata of experiment from DynamoDB'''
        pass


def query(filters: dict) -> dict:
    '''
    Function to query cellPortal experiments metadata table in AWS DynamoDB.

    Takes search parameters from search bar and/or filter as JSON/Dict format  
    and returns dictionary of items.
    '''
    pass