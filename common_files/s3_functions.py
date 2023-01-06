import boto3
s3 = boto3.client('s3')

def upload_image_to_s3(filepath,name):
    with open(filepath, "rb") as f:
        s3.upload_fileobj(f, "recipe-tasveers", filepath)