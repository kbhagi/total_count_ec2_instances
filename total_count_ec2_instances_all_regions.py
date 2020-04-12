__author__ = "Bhargava K"
__copyright__ = "Copyright 2019"
__credits__ = ["Bhargava"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Bhargava"
__email__ = "bhargavak37@gmail.com"
__status__ = "Development"

import boto3
import traceback
import argparse


def get_aws_account_session(profile_name):
    try:
        aws_account_session = boto3.Session(profile_name=profile_name)
        return aws_account_session
    except Exception:
        traceback.print_exc()


def count_total_instances(boto3_account_session, aws_regions):
    try:
        if not boto3_account_session and aws_regions:
            return
        sts_client = boto3_account_session.client('sts')
        account_id = sts_client.get_caller_identity()["Account"]
        instances_id = []
        for region in aws_regions:
            conn = boto3_account_session.resource('ec2', region_name=region)
            instances = conn.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
            for instance in instances:
                instances_id.append(instance.id)
                print(instance.id, instance.instance_type, region, account_id)

        return len(instances_id)
    except Exception:
        traceback.print_exc()


def lambda_handler(events,context):
    aws_profiles=events.get('aws_profiles')
    region=events.get('regions')
    aws_profile_names = aws_profiles.split(',')
    regions_list = region.split(',')
    print("Sessions ", aws_profile_names)
    instances_count  = 0
    for aws_profile_name in aws_profile_names:
        aws_account_session = get_aws_account_session(aws_profile_name)
        instances_count += count_total_instances(aws_account_session, regions_list)
    print('total ec2 instances are : ', instances_count)
