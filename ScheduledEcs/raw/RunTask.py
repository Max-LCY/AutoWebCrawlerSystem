import boto3
import os
import time


AUTOSCAL = os.environ['AUTOSCAL']
CLUSTER = os.environ['ECS']
TASK = os.environ['TASKDEF']

def lambda_handler(event, context):
    # TODO implement
    try:
        set_autoscaling(AUTOSCAL)
        time.sleep(300)
        run_task(CLUSTER, TASK)
    except:
        raise
        
def set_autoscaling(Name):
    auto = boto3.client('autoscaling')
    
    auto.set_desired_capacity(
        AutoScalingGroupName=Name,
        DesiredCapacity=1)
    
def run_task(Name, task):
    ecs = boto3.client('ecs')
    
    ecs.run_task(
        cluster=Name,
        taskDefinition=task)
