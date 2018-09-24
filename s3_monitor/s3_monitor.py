from __future__ import absolute_import, division, print_function
import argparse
import boto3
import botocore
from datetime import datetime, timedelta

def connect_to_s3():
    """ Function to get AWS connection object 
        >> returns a connection for exploring the resources 
    """
    return boto3.resource('s3')

def get_buckets(conn):
    """ Get the names of the S3 Buckets
        >> returns a dictionary with the keys as bucket names and value as dictionary holding the details of the bucket. 
    """
    buckets_dict={}
    s3client = boto3.client('s3')
    allbuckets = s3client.list_buckets()
    for bucket in allbuckets['Buckets']:
        buckets_dict[bucket['Name']]=get_bucket_details(conn,buckets_dict,bucket)
    return buckets_dict

def get_bucket_details(conn,buckets_dict,bucket):
    """ Get the details of each bucket like size, cost etc.
        >> returns a dictionary with the bucket details
    """
    bucket_dict={}
    s3_client = boto3.client('s3')
    bucket_name=bucket['Name']
    bucket_object = conn.Bucket(bucket_name)
    bucket_dict["creation_date"]=bucket["CreationDate"]
    bucket_dict["total_size"]=sum([object.size for object in boto3.resource('s3').Bucket(bucket_name).objects.all()])
    bucket_dict["no_of_files"]=sum(1 for _ in bucket_object.objects.all())
    objs=s3_client.list_objects_v2(Bucket=bucket_name)['Contents']
    get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
    sorted_objects=[obj for obj in sorted(objs, key=get_last_modified)]
    bucket_dict["last_modified"]=sorted_objects[-1]['LastModified']
    bucket_dict["creation_date"]=bucket["CreationDate"]
    print(bucket_dict)
    return bucket_dict

def cost_explorer():
    """ Get the AWS S3 billing details
        >> returns the monthly cost for each account """



def main():
     parser = argparse.ArgumentParser(description="Monitor the details of AWS S3 buckets.")
     parser.add_argument("--size")
     parser.add_argument("--type")
     parser.add_argument("--filter")
     parser.add_argument("--groupby")
     args=parser.parse_args()
     conn=connect_to_s3()
     get_buckets(conn)

if __name__=="__main__":
    main()
