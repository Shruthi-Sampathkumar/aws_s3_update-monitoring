import boto3
import hashlib
import time


s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

hashed_dict = {}
hash_suffix = "-hash"
AWS_BUCKET_NAME = "cloud-webtracker"


while(1):

    objects = s3_client.list_objects_v2(Bucket=AWS_BUCKET_NAME)
    for obj in objects['Contents']:
        key = obj["Key"]
        body = s3_resource.Object(AWS_BUCKET_NAME, key).get()['Body'].read()
        if key[-5:] != hash_suffix:
            #print("\nUnhashed key found")
            if key not in hashed_dict:
                hashed_dict[key]=1
                #print("\nContent not seen in the past found")
                html = body
                hashed_html = hashlib.sha256(html).hexdigest()
                s3_resource.Object(AWS_BUCKET_NAME, key).delete()
                #print("\nUnhashed content removed from s3 bucket")
                key+=hash_suffix
                s3_client.put_object(Body=hashed_html, Bucket=AWS_BUCKET_NAME, ContentType="text/html", Key=key, ACL="public-read")
                #print("\nHashed content added to s3 bucket")
            else:
                #print("\nContent seen in the past found")
                html = body
                hashed_html = hashlib.sha256(html).hexdigest()
                s3_resource.Object(AWS_BUCKET_NAME, key).delete()
                #print("\nUnhashed old content removed from s3 bucket")
                key+=hash_suffix
                s3_client.put_object(Body=hashed_html, Bucket=AWS_BUCKET_NAME, Key=key, ContentType="text/html", ACL="public-read")
                #print("\nOld hashed content is replaced with new hashed content")
        #else:
            #print("\nHashed content found. So continue to next object")
    time.sleep(10)