
from Person import *

class Contact(Person):
	"""
	An Object Representation of a Contact
	"""

	def __init__(self, data):
		Person.__init__(self, data)

		"""
		Constructor to initialize attributes pertainint to a contract
		"""
		self.attrs 	= {'id':'', 'owner_id':'', 'contact_nickname':'', 'phone':''}
		self.id 	= data['id']
		self.person_id = data['owner_id']
		self.valid 	= False	
		self.data 	= data
		self.phones = []



	def set_data(self):
		"""
		This function sets the data of a contact, and cleanse its phone numbers
		"""
		valid_fields = self.validate_fields()
		if valid_fields:
			self.attrs['id'] = self.id
			for field in self.attrs.keys(): self.attrs[field] = self.data[field]
		
			for phone in self.attrs['phone']:
				# print(phone)
				number = phone['number']
				clean_number = re.sub(r'\W', '', number)
				if len(clean_number) < 11: clean_number = '1'+clean_number
				# print(number, ' -> ', clean_number)
				self.phones.append(clean_number)
			return True




