import boto3
from misc import Misc
from time import sleep
import traceback
import sys

class AwsResource(object):
	""" docstring """
	def __init__(self, region, resource='ec2'):
		super(AwsResource, self).__init__()
		self.region = region
		self.resource = boto3.resource(resource, region_name=self.region)

	def create_instances(self, instance_type, image_id, key_pair_path, minCount = 1, maxCount = 1, subnet_id='subnet-02ce134a'):
		"""docstring"""

		try:

			key_pair = Misc.remove_extensions((Misc.get_filename_from_path(key_pair_path)))

			ec2 = self.resource

			instances = ec2.create_instances(
			     ImageId=image_id,
			     MinCount=minCount,
			     MaxCount=maxCount,
			     InstanceType=instance_type,
			     SubnetId=subnet_id,
			     KeyName=key_pair
			 )

			instance = instances[0]
			print("Created instance:", instance.instance_id)
			instance.wait_until_running()
			instance.reload()
			print("Current Instance State:", instance.state)
			sleep(30)                            # time for aws to register the instance_id

		except Exception as e:
			if hasattr(e, 'message'):
				print("Error occured: ", e.message)
			else:
				print("Error occured: ", e)
			traceback.print_exc(file=sys.stdout)

		return instances

	def delete_instances(self, instances):
		""" docstring """
		instance_ids = [x.instance_id for x in instances]
		self.resource.instances.filter(InstanceIds = instance_ids).terminate()
		print("Deleted instance:", instance_ids)
