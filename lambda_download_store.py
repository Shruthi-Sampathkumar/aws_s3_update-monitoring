import json
from urllib.request import urlopen
import boto3

def lambda_handler(event, context):
    # TODO implement
    url = event['queryStringParameters']['key']
    url_key = url.replace("/", "-")
    #print("\nthe user input url is ", url_key)
    AWS_BUCKET_NAME = 'cloud-webtracker'
    s3 = boto3.client('s3')
    with urlopen(url) as response:
        html = response.read()
        
    s3.put_object(Body=html, Bucket=AWS_BUCKET_NAME, ContentType = "text/html", Key=url_key, ACL="public-read")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Unhashed webpage is downloaded and stored in S3 Bucket named cloud-webtracker!')
    }