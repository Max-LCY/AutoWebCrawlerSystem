import boto3
import os

AUTOSCAL = os.environ['AUTOSCAL']

def lambda_handler(event, context):
    try:
        set_autoscaling(AUTOSCAL)
    except:
        raise
    
def set_autoscaling(Name):
    auto = boto3.client('autoscaling')
    
    auto.set_desired_capacity(
        AutoScalingGroupName=Name,
        DesiredCapacity=0)