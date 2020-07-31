import argparse

class ContactBook():
	
	def __init__(self):
		self.first = None
		self.last = None
		self.phone_number = None
		self.contact_book_dict = {}
		self.entry_type = None
		self.updated_phone = None

	def new_contact(self, first_n, last_n, phone):
		'''dict = {(last name, first name): phone number, (Ali, Zainab): 1110001234} '''
		self.first = first_n
		self.last = last_n
		self.phone_number = phone
		self.contact_book_dict[(self.last, self.first)] = self.phone_number
		if self.first != None and self.last != None and self.phone_number != None:
			print("Entry added!")		
			print(self.contact_book_dict)

	def update_contact(self, first_n, last_n, phone):
		print('updating contact')
		self.updated_phone = phone
		self.contact_book_dict[(last_n, first_n)] = self.updated_phone
		print(self.last_n, self.first_n, 'updated to: ', self.updated_phone)

	def delete_contact(self, first_n, last_n, phone):
		answer = input('Are you sure you want to delete the contact? (Y/N)')
		if answer == 'Y':
			try:			
				del self.contact_book_dict[(last_n, first_n)]
			except:
				print("This contact does not exist")
		elif answer == 'N':
			answer_2 = input("Would you like to enter a new contact? (Y/N)")
			if answer_2 == 'Y':
				self.new_contact(first_n, last_n, phone)
			else:
				pass
		else:
			pass

	def ask_user(self, first_n, last_n, phone, entry_type):
		self.entry_type = entry_type
		if self.entry_type == 1:
			self.new_contact(first_n, last_n, phone)
		elif self.entry_type == 2:
			self.update_contact(first_n, last_n, phone)
		elif self.entry_type == 3:
			self.delete_contact(first_n, last_n, phone)
		else:
			pass

def main():
	parser = argparse.ArgumentParser(description='Enter information to create a new entry in the contact book.')
	parser.add_argument('-f', '--first', type=str, metavar='', required=True, help='Enter first name')
	parser.add_argument('-l', '--last', type=str, metavar='', required=True, help='Enter last name')
	parser.add_argument('-p', '--phone', type=int, metavar='', help='Enter phone number')
	parser.add_argument('-e', '--entry_type', type=int, metavar='', help='1 = new entry, 2 = update entry, 3 = delete')
	args = parser.parse_args()

	contact_book = ContactBook()
	contact_book.ask_user(args.first, args.last, args.phone, args.entry_type)

if __name__ == '__main__':
	main()
