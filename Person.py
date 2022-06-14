
import re

class Person(object):
	"""
		An object representation of a Person Entity
	"""



	def __init__(self, data):

		"""
		Constructor to initialize attributes pertainint to a Person

		:param : 
		:type : 
		:return:
		:rtype:
		"""
		self.attrs 	= {'id':'', 'first':'', 'last':'', 'phone':'', 'experience':''}
		self.id 	= data['id']
		self.valid 	= False	
		self.data 	= data
		self.checks = {}	



	def set_names(self):
		if self.checks['fields']:
			self.attrs['id'] = self.id
			self.attrs['last'] = self.data['last']
			self.attrs['first'] = self.data['first']
			self.name = self.data['first']+' '+self.data['last']
			self.company = self.attrs['experience'][0]['company']
		
			return True



	def validate_fields(self):
		self.checks['fields'] = True
		for field in self.data.keys():
			if 	field.lower() not in self.attrs.keys():
				self.checks['fields'] = False
				break
			else: self.checks[field.lower()] = False
		return self.checks['fields']


	def validate_fields(self):
		self.checks['fields'] = True
		for field in self.data.keys():
			if 	field.lower() not in self.attrs.keys():
				self.checks['fields'] = False
				break
			else: self.checks[field.lower()] = False
		return self.checks['fields']



	def validate_phone(self):
		if self.checks['fields']:
			if 	re.search(r'null|\d+-\d+', self.data['phone']):
				self.checks['phone']= True
				self.attrs['phone'] = self.data['phone']
		
		return self.checks['phone']



	def validate_experience(self):
		if self.checks['fields']:
			fields = self.data['experience'][0].keys()
			if 	'start' in fields and 'end' in fields:
				start = self.data['experience'][0]['start']
				end = self.data['experience'][0]['end']
				if re.search(r'\d{4}-\d{2}-\d{2}', start):
					if re.search(r'\d{4}-\d{2}-\d{2}|None', str(end)) :
						self.checks['experience']= True
						self.attrs['experience'] = self.data['experience']
						# if not end:
						# 	self.attrs['experience'][0]['end'] = dt.today().strftime('%Y-%m-%d')
		
		return self.checks['experience']



	def validate(self):
		valid_fields = self.validate_fields()
		valid_phone = self.validate_phone()
		valid_experience = self.validate_experience()
		if valid_fields and valid_phone and valid_experience:
			self.valid = True

		self.set_names()

		# print('has all fields: ', valid_fields)
		# print('has valid phone: ', valid_phone)
		# print('has valid experience: ', valid_experience)
		return self.valid



	def __repr__(self):

		"""

		:param :
		:type : 
		"""
		
		return json.dumps(self.attrs, indent=4)
