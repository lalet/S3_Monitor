from __future__ import absolute_import, division, print_function
import argparse
import boto3
import botocore
from datetime import datetime, timedelta
from botocore.exceptions import ClientError
import re

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
    #Create s3 client
    s3_client = boto3.client('s3')
    allbuckets = s3_client.list_buckets()
    for bucket in allbuckets['Buckets']:
        buckets_dict[bucket['Name']]=get_bucket_details(conn,s3_client,buckets_dict,bucket)
    return buckets_dict

def get_bucket_details(conn,s3_client,buckets_dict,bucket):
    """ Get the details of each bucket like size, cost etc.
        >> returns a dictionary with the bucket details
    """
    bucket_dict={}
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
    cost_explorer()
    return bucket_dict

def cost_explorer():
    """ Get the AWS S3 billing details
        >> returns the monthly cost for each account """
    # Create a Cost Explorer client
    cost_client = boto3.client('ce')
    
    # Set time range to cover the last full calendar month
    # Note that the end date is EXCLUSIVE (e.g., not counted)
    now = datetime.utcnow()
    
    # Set the end of the range to start of the current month
    end = datetime(year=now.year, month=now.month, day=1)
    
    # Subtract a day and then "truncate" to the start of previous month
    start = end - timedelta(days=1)
    start = datetime(year=start.year, month=start.month, day=1)
    
    # Convert them to strings
    start = start.strftime('%Y-%m-%d')
    end = end.strftime('%Y-%m-%d')
    
    #Get cost explorer response
    response = cost_client.get_cost_and_usage(
        TimePeriod={
            'Start': start,
            'End':  end
        },
        Granularity='MONTHLY',
        Metrics=['BlendedCost'],
        GroupBy=[
            {
                'Type': 'TAG',
                'Key': 'Project'
            },
        ]
    )
   
    print("Response")
    print(response)

    for project in response["ResultsByTime"][0]["Groups"]:
        namestring = project['Keys'][0]
        name = re.search("\$(.*)", namestring).group(1)
        if name is None or name == "":
            name = "Other"

        amount = project['Metrics']['BlendedCost']['Amount']
        amount = float(amount)
        line = "{}\t${:,.2f}".format(name, amount)
        print(line)

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
