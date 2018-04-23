import boto3


class Ec2Instance(object):
    def __init__(self):
        self.instance_name = 'ADD_INSTANCE_NAME_HERE'

    def get_instances(self):
        ec2 = boto3.client('ec2')
        return ec2.describe_instances()

    def find_instance(self):
        instances = self.get_instances()
        for i in instances['Reservations'][0]['Instances']:
            tags = i['Tags'][0]['Value']
            if tags == self.instance_name:
                return i['InstanceId']

    def ec2_instance(self):
        instance_id = self.find_instance()
        ec2 = boto3.resource('ec2')
        instance = ec2.Instance(instance_id)
        return instance
