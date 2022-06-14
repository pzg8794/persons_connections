import os
import re
import sys
import json

from Persons import *





def get_file_data(file_name='persons.json'):
	"""
	Function to get json data from a local file
	"""
	try: 
		persons_data = open(file_name, 'r')
		persons = json.load(persons_data)
		return persons
	except Exception as e: print(e)
	return []


if __name__ == "__main__":
	commands = sys.argv[1:]
	# print(commands)

	if not commands:
		print('You must provide a Person Id from the persons.json file located in this directory')
		print('i.e. python3 test_persons.py -id 0')

	else:
		try:
			person_id 			= int(commands[-1])

			persons 			= Persons()
			persons_data 		= get_file_data(file_name='persons.json')
			contacts_data 		= get_file_data(file_name='contacts.json')
			contacted_persons1 	= persons.get_connected_persons(persons_data, person_id)
			persons.display_persons(contacted_persons1)
			contacted_persons2 	= persons.get_connected_persons_by_contacts(contacts_data, person_id)
			persons.display_persons(contacted_persons2)
			# print(contacted_persons1)
			# print(contacted_persons2)
		except Exception as e:
			print('Person Id must be a digit from the persons.json file located in this directory')
			print('i.e. python3 test_persons.py -id 0\n', e)