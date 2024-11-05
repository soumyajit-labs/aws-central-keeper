import boto3
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv
load_dotenv()

region = os.environ['AWS_REGION']

def fetch(key):
    session = boto3.session.Session()
    client = session.client( service_name='secretsmanager', region_name=region )
    try:
        get_secret_value_response = client.get_secret_value( SecretId=key )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            return 404
        else:
            return 400

    secret = get_secret_value_response['SecretString']
    return secret

def upsert(key, val, user):
    print('User: ', user)
    session = boto3.session.Session()
    client = session.client( service_name='secretsmanager', region_name=region )
    try:
        updateRes = client.update_secret( SecretId=key, SecretString=val )
        updateTag = client.tag_resource( SecretId=key, Tags=[{ 'Key': 'UpsertedBy', 'Value': user }] )

        return 200
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            response = client.create_secret( Name=key, SecretString=val, Tags=[{ 'Key': 'UpsertedBy', 'Value': user }] )
            return 201
        else:
            return 400