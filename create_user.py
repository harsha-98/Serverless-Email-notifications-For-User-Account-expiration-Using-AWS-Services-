import json
import os
import uuid
import datetime
from datetime import date
import boto3
import random
import hashlib
from boto3.dynamodb.conditions import Key



dynamodb= boto3.resource('dynamodb')
table_name= "registeruser"
table=dynamodb.Table(table_name)


def lambda_handler(event, context):

    email_address=event['emailId']
    first_name=event['firstName']
    last_name=event['lastName']
    password=event['password']
    
    email_arr=[]
    resp = table.scan(AttributesToGet=['emailId'])
    for i in resp['Items'] :
        email_arr.append(i['emailId'])

    if email_address in email_arr:
        return {
        "statusCode" : 200,
        "body":json.dumps("Email id already exists"),
        "status" : "duplicate"
        }

    new_user=__create_user(first_name,last_name,email_address,password)

    return{

        "statusCode" : 200,
        "body": json.dumps(new_user),
        "status": "new"
        }

def __create_user(first_name,last_name,email_address,password):
    print("using dynamo table:" + table_name)

    register_date=(date.today()).strftime("%m-%d-%Y")
    
    expiryDate = (date.today()+datetime.timedelta(days=30)).strftime('%m-%d-%Y')
    print(register_date)
    print(expiryDate)
    temp=str(password)
    print(password)
    
    encrypt_password=hashlib.sha256(password.encode()).hexdigest()
    print(encrypt_password)
    


    print("writing user")
    user_details=table.put_item(
        TableName=table_name,
        Item={
            'emailId':email_address,
            'expiryDate':str(expiryDate),
            'firstName':first_name,
            'lastName':last_name,
            'registrationDate': register_date,
            'password':encrypt_password
        },
    )
    
    return user_details
