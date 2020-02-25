import time, datetime

class Misc:

	def __init__(self):
		pass

	def get_filename_from_path(path):
		return path.split('/')[-1]

	def remove_extensions(filename):
		return filename.split('.')[0]

	def find_and_replace(fpath, find, replace):

		with open(fpath, 'r') as file :
			filedata = file.read()
			filedata = filedata.replace(find, replace)

			with open(fpath, 'w') as file:
				file.write(filedata)

	def none_safe(arg, returning = '', type=str):
		if not isinstance(arg, type):
			arg = type(arg)
		return arg if arg else returning

	def time_now():
		current_time = time.time()
		return datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')


