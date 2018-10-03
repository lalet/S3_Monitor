import unittest
import boto3
from moto import mock_s3
import argparse
from s3_monitor import *

class S3MonitorTestCase(unittest.TestCase):

    def setUp(self):
        """ Setup will run before execution of each test case """ 
        self.bucket = "business"
        self.key="mock"
        self.value="value"

    
    @mock_s3
    def __moto_setup(self):
        """ Simulate s3 upload """
        conn = boto3.client('s3')
        conn.create_bucket(Bucket=self.bucket)
        conn.put_object(Bucket=self.bucket, Key=self.key, Body=self.value)
    
    def test_get_client(self):
        """ Ensure that the end point is the same as AWS """
        conn=boto3.client('s3')
        self.assertEqual(conn._endpoint.host,  'https://s3.amazonaws.com')
    
    @mock_s3
    def test(self):
        #setup s3 env
        self.__moto_setup()
        args = argparse.Namespace()
        args.groupby=None
        args.filter=None
        buckets = [b for b in get_buckets(boto3.client('s3'),args)]
        print(buckets)
