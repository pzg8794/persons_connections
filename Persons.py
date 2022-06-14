

import re
from datetime import datetime as dt

from Person import *
from Contact import *


class Persons(object):
	"""
		An object representation of a group of objects of type Person and/or Contact, used to manage the data from each entity
	"""



	def __init__(self):

		"""
		Constructor to initialize attributes pertaining to a person and a contact
		"""

		self.attrs = {'persons':{}, 'contacts':{}}
		self.objs = {'persons':{}, 'contacts':{}, 'companies':{}, 'persons_contacts':{}}



	def contains(self, person):
		"""
		This function checks if a Person being added already exists
		i.e. there will not be multiple entries for the same person/company
		"""
		for _id, _person in self.objs['persons'].items():
			if person.name == _person.name:
				if person.company == _person.company:
					return True
		return False



	def add_person(self, person_data):
		"""
		Function to create and add a Person Object
		"""
		person = Person(person_data)
		is_valid = person.validate()
		# print(person_data)
		# print("Is Person's Data Valid: ", is_valid)
		# print(person)
		if is_valid and not self.contains(person): 
			self.objs['persons'][person.id] = person
			if person.company in self.objs['companies'].keys():
				self.objs['companies'][person.company].append(person.id)
			else: self.objs['companies'][person.company] = [person.id]
		else: #already contains person
			pass



	def add_contact(self, person_data, entity='contacts'):
		"""
		Function to create and add a contact to a person
		"""
		contact = Contact(person_data)
		contact.set_data()
		# print(person_data)
		# print(contact)
		if contact.id not in self.objs[entity].keys(): 
			self.objs[entity][contact.id] = contact
			if contact.person_id not in self.objs['persons_contacts'].keys():
				self.objs['persons_contacts'][contact.person_id] = [contact.id]
			else: self.objs['persons_contacts'][contact.person_id].append(contact.id)
		else: #already contains person
			pass



	def load_persons_entities(self, persons, entity='persons', msg='PART I - Loading '):
		"""
		Function to load an entity data to memory, the entity can be either a person or a contact
		"""
		print('\n', '*'*150,'\n', msg, entity,'\n','*'*150)	
		if 	persons:
			for person in persons:
				fields = [key.lower() for key in person.keys()]
				if 'id' in fields:
					if person['id'] not in self.attrs[entity].keys():
						self.attrs[entity][person['id']] = person
						if entity == 'persons': self.add_person(person)
						elif entity == 'contacts': self.add_contact(person)
						# print(person)
					else: #duplicate person id
						pass
			return True



	def get_connected_persons(self, persons, person_id, msg='PART II - Loading Persons Connected'):
		"""
		Function to get Persons connected by the company and  time
		i.e. Two Persons are connected if they worked for the same company and their timelines at the company overlap by at least 90 days
		"""
		connected_persons = []
		if self.load_persons_entities(persons):
			print('\n', '*'*150,'\n', msg,'\n','*'*150)	
			if person_id in self.objs['persons'].keys():
				person = self.objs['persons'][person_id]
				# print(person)

				for experience in person.attrs['experience']:
					company = experience['company']
					p_start = dt.strptime(experience['start'], "%Y-%m-%d") 
					p_end = experience['end'] 
					# note: null values for “end” mean the present
					if not experience['end']: p_end = dt.today().strftime('%Y-%m-%d')
					p_end = dt.strptime(p_end, "%Y-%m-%d") 
					p_days = (p_end - p_start).days

					if p_days < 90: continue

					for _person_id in self.objs['companies'][company]:
						if _person_id == person_id: continue

						_person = self.objs['persons'][_person_id]
						_experiences = _person.attrs['experience']
						for _experience in _experiences:
							start = dt.strptime(_experience['start'], "%Y-%m-%d") 
							end = _experience['end'] 
							if not _experience['end']: end = dt.today().strftime('%Y-%m-%d')
							end = dt.strptime(end, "%Y-%m-%d")
							days = (end - start).days

							is_a_contact = False
							if days < 90: continue

							if 		start <= p_start and end >= p_end: is_a_contact = True
							elif 	start > p_start and end < p_end: is_a_contact = True
							elif 	start <= p_start and end < p_end: 
								_days = (end - p_start).days
								if _days >= 90: is_a_contact = True

							elif 	start > p_start and end >= p_end: 
								_days = (p_end - start).days
								if 	_days >= 90: is_a_contact = True

							if is_a_contact:
								# print(_person)
								# print(days)
								connected_persons.append(_person_id)

		return connected_persons



	def get_connected_persons_by_contacts(self, persons, person_id, msg='PART III - Loading Persons Connected by Contacts'):
		"""
			Function to get Persons connected by Contacts
			i.e. two Persons are connected when either one has the other’s phone number in their list of contacts.
		"""
		connected_persons = []
		if self.load_persons_entities(persons, entity='contacts'):
			print('\n', '*'*150,'\n', msg,'\n','*'*150)	
			if 	person_id in self.objs['persons_contacts'].keys():
				contact_ids = self.objs['persons_contacts'][person_id]

				p_contact_numbers = []
				for contact_id in contact_ids:
					contact = self.objs['contacts'][contact_id]
					p_contact_numbers += contact.phones

				# print(p_contact_numbers)
				for _person_id, contacts in self.objs['persons_contacts'].items():
					if _person_id 	== person_id: continue
					for contact_id 	in contacts:
						contact 	= self.objs['contacts'][contact_id]
						has_number 	= False
						# print(contact)
						for phone in contact.phones:
							# print(phone)
							if phone in p_contact_numbers: 
								has_number = True
								connected_persons.append(_person_id)
								break
						if has_number: break
		return connected_persons



	def display_persons(self, persons_id, msg='PART IV - Loading Persons Connected by Contacts'):
		"""
			Function to print Persons as per requirements
			i.e. print out the list of connected persons (ID: First Last, one per line) to the console, ordered by ID
		"""
		print('\n', '*'*150,'\n', msg,'\n','*'*150)	

		persons_id = sorted(persons_id)
		for person_id in persons_id:
			person = self.objs['persons'][person_id]
			print(person_id, ':', person.name)



