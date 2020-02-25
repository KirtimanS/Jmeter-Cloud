from aws_resource import AwsResource
from secure_connection import SecureConn
from misc import Misc
import traceback
from jmx_editor import JmxEditor
import sys

class Core(object):
	"""docstring for Core"""
	def __init__(self, args):

		self.args = args
		self.cmds = ['cd jmeter',
        			'sudo yum -y install java-1.8.0-openjdk',
        			'wget -c http://mirror.cc.columbia.edu/pub/software/apache//jmeter/binaries/apache-jmeter-5.2.1.tgz', 
        			'tar -xf apache-jmeter-5.2.1.tgz',
        			'apache-jmeter-5.2.1/bin/./jmeter -n -t /home/ec2-user/jmeter/'+Misc.get_filename_from_path(self.args.test_plan)+' -l /home/ec2-user/jmeter/'+self.args.log]

	def run(self):

		try:
			jmx_modifiers = {'iterations': self.args.iter, 'threads': self.args.threads}
			if any(data for mod, data in jmx_modifiers.items()):
				jmx_editor = JmxEditor(self.args.test_plan)
				jmx_editor.change_jmx(jmx_modifiers)

			resource = AwsResource(self.args.region)
			instances = resource.create_instances(self.args.instance, self.args.ami, self.args.key)
			conn = SecureConn(self.args.key, instances[0].private_ip_address)
			conn.send_commands(self.cmds, self.args.test_plan, self.args.csv)

		except Exception as e:

			if hasattr(e, 'message'):
				print("Error occured: ", e.message)
			else:
				print("Error occured: ", e)
			traceback.print_exc(file=sys.stdout)

		finally:
			if instances and self.args.del_ins == "Y":
				resource.delete_instances(instances)

if __name__ == '__main__':
	run()
		