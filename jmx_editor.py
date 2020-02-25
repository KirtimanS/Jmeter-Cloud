import xml.etree.ElementTree as ET
import sys
import json
from misc import Misc
import argparse

class JmxEditor:

	def __init__(self, jmx_path):
		self.jmx = jmx_path
		self.tree = ET.parse(self.jmx)
		self.root = self.tree.getroot()

	def change_jmx(self, modifiers):
		test_plan_elems = { 'iterations':"${__P(iterations,"+ Misc.none_safe(modifiers.get('iterations'))+")}",
							'threads':"${__P(threads,"+Misc.none_safe(modifiers.get('threads'))+")}"}

		modify_data = {}
		for mod, data in modifiers.items():
			if mod in test_plan_elems and data:
				modify_data[mod] = test_plan_elems[mod]

		return self.edit_jmx(modify_data)


	def edit_jmx(self, mod_data):
		jmx_elems = {'iterations':'LoopController.loops', 
		'threads':'ThreadGroup.num_threads'}

		jmx_new_data = {}
		for attribute, data in mod_data.items():
			if attribute in jmx_elems:
				jmx_new_data[jmx_elems[attribute]] = data

		print('\n')

		for child in self.root.iter('stringProp'):
			if child.attrib['name'] in jmx_new_data:
				prop_name = child.attrib['name']
				child.text = jmx_new_data[prop_name]
				print("Modification: ", prop_name, " Data: ", child.text)


		self.tree.write(self.jmx, encoding="UTF-8", xml_declaration=True)

		print('\n')



if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Edit JMeter load test file .jmx')
	parser.add_argument('--tp', '--testPlan', required=True, dest='test_plan', metavar='\b', help='complete path to a JMeter testplan')
	parser.add_argument('--m', '--modifiers', type=json.loads, required=True, dest='mods', metavar='\b', help='test plan attributes to modify (enter a json like so --> "{"threads":100}"")')
	args = parser.parse_args()

	jmx_editor = JmxEditor(args.test_plan)
	jmx_editor.change_jmx(args.mods)