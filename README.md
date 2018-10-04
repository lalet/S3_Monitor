# S3_Monitor
Script to monitor S3 metadata

# S3_Monitor
Script to monitor S3 metadata

##### *Pre-requisites* :
###### 1. Install the plugin and the credentials
* Install boto
* Set up the AWS credentials ([Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html))

###### 2. Create a Policy that allows access to the Cost Explorer API :
 1. IAM > Policies > Create policy
 2.  Service: Cost Explorer Service
 3. Actions: All
 4. Name: allowCostExplorerRead
 
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "ce:*",
            "Resource": "*"
        }
    ]
} 
```
###### 3. Bundle these policies to the role that is being used :
1. IAM > Roles > Search "<role>"
2. Attach policy:
  - [x] allowCostExplorerRead

##### The tool returns the below given details :
* Bucket name
* Creation date (of the bucket)
* Number of files
* Total size of files
* Last modified date (most recent file of a bucket)
* And how much does it cost for the current month

##### Documentation
usage: s3_monitor.py [-h] [--size SIZE] [--type TYPE] [--filter FILTER] [--groupby GROUPBY]

Monitor the details of AWS S3 buckets.
optional arguments:
  --size SIZE :  KB, MB, GB (Default size is bits)
  --type TYPE : Filter based on instance types (Standard, AA, ...)
  --filter FILTER : (Not fully implemented - regex support)
  --groupby GROUPBY : (Filter based on regions)

###### Sample code and output
``` s3_monitor.py --groupby sa-east-1 --size MB ```
```
{'lal-business': {'creation_date': '2018-09-24', 'total_size': 0, 'no_of_files': 3, 'last_modified': '2018-09-24', 'cost': 0.0049999816}}
```





