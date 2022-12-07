import json
import boto3
import datetime
from datetime import date
from botocore.exceptions import ClientError

def lambda_handler(event, context):

    dataSource = boto3.resource('dynamodb')
    table = dataSource.Table('registeruser')

    try:
        
        result = table.scan()
        data = result['Items']
    except:
        raise

    expirationDate = (date.today()+datetime.timedelta(days=7)).strftime('%m-%d-%Y')
        
    for record in data:
        #if(record ['expiryDate'] == expirationDate ):
        if(False):
            
            SENDER = "coandcloud@gmail.com"
            RECIPIENT = record['emailId']
            NAME = record['firstName']

            AWS_REGION = "us-east-1"

            SUBJECT = "Your Cloud & Co., subscription is expring soon!" 
                
            BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                            "This email was sent with Amazon SES using the "
                            "AWS SDK for Python (Boto)."
                            )
                            
            BODY_HTML = f"""<html>
                <head></head>
                <body>
                  <p>Dear {NAME},</p>
                  <p>Your Cloud & Co. subscription is expring on {expirationDate}.</p>
                  <p>This email was sent with
                    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
                    <a href='https://aws.amazon.com/sdk-for-python/'>
                      AWS SDK for Python (Boto)</a>.</p>
                </body>
                </html>
                            """            
            
            CHARSET = "UTF-8"
                
            client = boto3.client('ses',region_name=AWS_REGION)
                
            try:

                #Provide the contents of the email.
                response = client.send_email(
                    Destination={
                        'ToAddresses': [
                            RECIPIENT,
                        ],
                    },
                Message={
                        'Body': {
                            'Html': {
                                'Charset': CHARSET,
                                'Data': BODY_HTML,
                            },
                            'Text': {
                                'Charset': CHARSET,
                                'Data': BODY_TEXT,
                            },
                        },
                        'Subject': {
                            'Charset': CHARSET,
                            'Data': SUBJECT,
                            },
                    },
                Source=SENDER
                )
            except ClientError as e:
               return ((e.response['Error']['Message']))
        else:
             continue
            