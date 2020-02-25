import paramiko
from subprocess import Popen, PIPE, STDOUT
import sys
import traceback
from misc import Misc
import time

class SecureConn:

	def __init__(self, key_path, private_ip, metric="percentage"):
		self.disp_metric = metric
		self.key_path = key_path
		self.private_ip = private_ip


	def move_files_scp(self, file_paths, direction):

		if direction == 'upload':
			command = ["scp","-i", self.key_path, file_paths, ] 
		elif direction == 'download': 
			command = ["scp", "-i", self.key_path]
		else:
			raise LookUpError("File movement direction invalid. Choose from 'Upload' and 'Download'.")

		for paths in file_paths:
			p = Popen(command, stdout = PIPE, stderr = STDOUT, shell = True)
			while True:
				line = p.stdout.readline().decode('utf-8')
				if not line:	break
				print(line)
			## TODO: add logger



	def send_commands(self, cmds, test_plan, test_data, result_log_name ='log.jtl', log_name='jmeter.log', default_username="ec2-user"):

		prefix = ''
		if result_log_name == 'log.jtl':
			prefix = Misc.remove_extensions(Misc.get_filename_from_path(test_plan))+'_'+Misc.time_now()+'_' 

		with paramiko.SSHClient() as client:
			key = paramiko.RSAKey.from_private_key_file(self.key_path)        
			client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

			try:
				client.connect(hostname=self.private_ip, username=default_username, pkey=key)
				self.execute_commands(client, ["echo 'Connected to EC2 instance'"])          # connection acknowledgement 

				self.execute_commands(client, ["mkdir jmeter"])                              # create separate directory
				ftp_client = client.open_sftp()
				print("Starting Jmeter config file upload:" , Misc.get_filename_from_path(test_plan))
				ftp_client.put(test_plan, '/home/ec2-user/jmeter/'+Misc.get_filename_from_path(test_plan), callback=self.print_transfer_status)
				print("Jmeter config (.jmx) file uploaded.")
				if test_data:
					print("Starting test data CSV file upload:" , Misc.get_filename_from_path(test_data))
					ftp_client.put(test_data, '/home/ec2-user/jmeter/'+Misc.get_filename_from_path(test_data), callback=self.print_transfer_status)
					print("Test Data (.csv) uploaded.")


				self.execute_commands(client, cmds)

				print('Starting Jmeter log (.log) file download')
				ftp_client.get('/home/ec2-user/'+log_name, prefix+log_name, callback=self.print_transfer_status)
				print("JMeter log (.log) file downloaded as :", prefix+log_name)
				print("Starting Jmeter results file (.jtl) download.")
				ftp_client.get('/home/ec2-user/jmeter/'+result_log_name, prefix+result_log_name, callback=self.print_transfer_status)
				print("JMeter results (.jtl) file downloaded as :", prefix+result_log_name)
				ftp_client.close()


			except Exception as e:
				if hasattr(e, 'message'):
					print("Error occured: ", e.message)
				else:
					print("Error occured: ", e)
				traceback.print_exc(file=sys.stdout)

	def execute_commands(self, client, cmds):       

		for cmd in cmds:
			stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
			while True:
				line = stdout.readline()
				if not line:
					break
				print(line)
		return stdout




	def print_transfer_status(self, transferred, toBeTransferred):

		if self.disp_metric == "percentage":
			print("File transferred: {0:.0f} %".format((transferred / toBeTransferred) * 100), end="\r", flush=True)
		elif self.disp_metric == "absolute":
			print("File transferred: ", transferred, "out of ", toBeTransferred)
		else:
			raise LookUpError("Status display metric not found. Choose from 'percentage' and 'absolute'")

if __name__ == "__main__":
	send_commands(sys.argv)


