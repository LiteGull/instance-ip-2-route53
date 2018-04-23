import boto3

from src.Ec2Instance import Ec2Instance


class HostedZone:
    def __init__(self):
        self.instance = Ec2Instance().ec2_instance()
        self.hosted_zone_name = 'ADD_DOMAIN_HERE'

    def all_hosted_zones(self):
        r53 = boto3.client('route53')
        return r53.list_hosted_zones()

    def get_zone(self):
        zones = self.all_hosted_zones()
        for i in zones['HostedZones']:
            if i['Name'] == self.hosted_zone_name:
                return i

    def create_a_record(self):
        zone = self.get_zone()
        r53 = boto3.client('route53')
        return r53.change_resource_record_sets(
            HostedZoneId=zone['Id'],
            ChangeBatch={
                'Comment': 'Public IP of instance',
                'Changes': [
                    {
                        'Action': 'CREATE',
                        'ResourceRecordSet': {
                            'Name': 'www.{}'.format(self.hosted_zone_name),
                            'Type': 'A',
                            'TTL': 300,
                            'ResourceRecords': [
                                {
                                    'Value': self.instance.public_ip_address
                                },
                            ],
                        }
                    },
                ]
            }
        )


if __name__ == "__main__":
    HostedZone().create_a_record()
