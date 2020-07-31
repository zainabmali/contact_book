import argparse
import sqlite3
from sqlite3 import Error

class ContactBook():
	
	def __init__(self):
		self.first = None
		self.last = None
		self.phone_number = None
		self.contact_book_dict = {}
		self.entry_type = None
		self.updated_phone = None
		self. connection = None
		
		try:
			self.connection = sqlite3.connect('contact_book.db')
		except Error as e:
			print(e)

		create_contact_table = """CREATE TABLE IF NOT EXISTS contacts (
			first_name VARCHAR(32) NOT NULL,
			last_name VARCHAR(32),
			phone_number VARCHAR(15) PRIMARY KEY );"""
																													
		self.execute_query(create_contact_table)

	def execute_query(self, query, vars=[]):
		try:
			c = self.connection.cursor()
			c.execute(query, vars)
		except Error as e:
			raise e
		self.connection.commit()
		return c.fetchall()

	def new_contact(self, first_n, last_n, phone):
		new_contact_query = """INSERT INTO contacts(
			first_name,
			last_name,
			phone_number) VALUES (?, ?, ?) """
		try:
			self.execute_query(new_contact_query, vars=[first_n, last_n, phone])
			print("\nContact successfully added!")
			print(first_n, last_n, phone, '\n')
		except Error as e:
			if e.args[0].startswith('UNIQUE constraint failed'):
				query_contact = """SELECT first_name, last_name FROM contacts WHERE phone_number = ?"""
				occupied_contact = self.execute_query(query_contact, vars=[phone])
				print('\nA contact with the name', occupied_contact[0][0], occupied_contact[0][1], 'is already assigned to this phone number\n')
			else:
				print(e)

	def update_contact(self, first_n, last_n, phone):
		print('updating contact')
		self.updated_phone = phone
		self.contact_book_dict[(last_n, first_n)] = self.updated_phone
		print(self.last_n, self.first_n, 'updated to: ', self.updated_phone)

	def delete_contact(self, first_n, last_n, phone):
		answer = input('Are you sure you want to delete the contact? (Y/N)')
		if answer == 'Y':
			try:			
				delete_contact_query = """DELETE FROM contacts WHERE phone_number = ?"""
				self.execute_query(delete_contact_query, vars=[phone])
				print('successfully deleted: ', first_n, last_n, phone)
			except Error as e:
				print(e)
				print("\nThis contact does not exist! Check your inputs.\n")
		elif answer == 'N':
			answer_2 = input("\nWould you like to enter a new contact? (Y/N)\n")
			if answer_2 == 'Y':
				self.new_contact(first_n, last_n, phone)
			else:
				pass
		else:
			pass

	def list_contacts(self):
		list_all_contacts_query = """SELECT * FROM contacts;"""
		all_contacts = self.execute_query(list_all_contacts_query)
		print(all_contacts)


	def ask_user(self, first_n, last_n, phone, entry_type):
		self.entry_type = entry_type
		if self.entry_type == 1:
			self.new_contact(first_n, last_n, phone)
		elif self.entry_type == 2:
			self.update_contact(first_n, last_n, phone)
		elif self.entry_type == 3:
			self.delete_contact(first_n, last_n, phone)
		elif self.entry_type == 4:
			self.list_contacts()
		else:
			pass

def main():
	parser = argparse.ArgumentParser(description='Enter information to create a new entry in the contact book.')
	parser.add_argument('-f', '--first', type=str, metavar='', required=True, help='Enter first name')
	parser.add_argument('-l', '--last', type=str, metavar='', required=True, help='Enter last name')
	parser.add_argument('-p', '--phone', type=int, metavar='', help='Enter phone number')
	parser.add_argument('-e', '--entry_type', type=int, metavar='', help='1 = new entry, 2 = update entry, 3 = delete, 4 = list_contacts')
	args = parser.parse_args()

	contact_book = ContactBook()
	contact_book.ask_user(args.first, args.last, args.phone, args.entry_type)

	if contact_book.connection:
		contact_book.connection.close()

if __name__ == '__main__':
	main()
