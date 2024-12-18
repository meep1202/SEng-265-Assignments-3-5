from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout, QTableView
from PyQt6.QtGui import QStandardItemModel, QStandardItem

from clinic.controller import Controller
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.gui.appointment_menu_gui import AppointmentMenuGUI

class MainMenuGUI():

	def __init__(self, main_window, controller):
		self.main_window = main_window
		self.controller = controller
		self.appointment_menu_gui = AppointmentMenuGUI(self, self.main_window, self.controller)
	
	# displays patient menu for different options
	def main_menu(self):
		# Clear window and set layout
		self.main_window.setCentralWidget(None) #<- use this code to clear window if needed to
		self.main_window.resize(250, 300)
		self.layout = QGridLayout()
		
		# Data input and labels
		self.create_patient = QPushButton("Create New Patient")
		self.search_patient = QPushButton("Search Existing Patient by PHN")
		self.search_patient_name = QPushButton("Search Patients by Name")
		self.update_patient = QPushButton("Update Existing Patient")
		self.delete_patient = QPushButton("Delete Existing Patient")
		self.list_all_patients = QPushButton("List All Existing Patients")
		self.start_appointment = QPushButton("Start Appointment")
		self.log_out = QPushButton("Log Out")
		
		# Adding Widgets
		self.layout.addWidget(self.create_patient, 0, 0)
		self.layout.addWidget(self.search_patient, 1, 0)
		self.layout.addWidget(self.search_patient_name, 2, 0)
		self.layout.addWidget(self.update_patient, 3, 0)
		self.layout.addWidget(self.delete_patient, 4, 0)
		self.layout.addWidget(self.list_all_patients, 5, 0)
		self.layout.addWidget(self.start_appointment, 6, 0)
		self.layout.addWidget(self.log_out, 7, 0)
		
		# Setup
		self.widget = QWidget()
		self.widget.setLayout(self.layout)
		self.main_window.setCentralWidget(self.widget)
		
		# Actions
		self.create_patient.clicked.connect(self.create_patient_button_clicked)
		self.search_patient.clicked.connect(self.search_patient_button_clicked)
		self.search_patient_name.clicked.connect(self.search_patient_name_button_clicked)
		self.update_patient.clicked.connect(self.update_patient_button_clicked)
		self.delete_patient.clicked.connect(self.delete_patient_button_clicked)
		self.list_all_patients.clicked.connect(self.list_all_patients_button_clicked)
		self.start_appointment.clicked.connect(self.start_appointment_button_clicked)
		self.log_out.clicked.connect(self.log_out_button_clicked)
		
	# displays fields for creating new patient
	def create_patient_button_clicked(self):
		# Clear window and set layout
		self.main_window.setCentralWidget(None)
		self.layout = QGridLayout()
		self.main_window.resize(450, 300)

		# Data input and labels
		self.label_phn = QLabel("PHN:")
		self.text_phn = QLineEdit()
		self.label_name = QLabel("Name:")
		self.text_name = QLineEdit()
		self.label_birthdate = QLabel("Birthdate (YYYY-MM-DD):")
		self.text_birthdate = QLineEdit()
		self.label_phone = QLabel("Phone:")
		self.text_phone = QLineEdit()
		self.label_email = QLabel("Email:")
		self.text_email = QLineEdit()
		self.label_address = QLabel("Address:")
		self.text_address = QLineEdit()

		# Buttons
		self.submit_button = QPushButton("Create Patient")
		self.cancel_button = QPushButton("Cancel")


		# Adding Widgets
		self.layout.addWidget(self.label_phn, 0, 0)
		self.layout.addWidget(self.text_phn, 0, 1)
		self.layout.addWidget(self.label_name, 1, 0)
		self.layout.addWidget(self.text_name, 1, 1)
		self.layout.addWidget(self.label_birthdate, 2, 0)
		self.layout.addWidget(self.text_birthdate, 2, 1)
		self.layout.addWidget(self.label_phone, 3, 0)
		self.layout.addWidget(self.text_phone, 3, 1)
		self.layout.addWidget(self.label_email, 4, 0)
		self.layout.addWidget(self.text_email, 4, 1)
		self.layout.addWidget(self.label_address, 5, 0)
		self.layout.addWidget(self.text_address, 5, 1)
		
		self.layout.addWidget(self.submit_button, 12, 1)
		self.layout.addWidget(self.cancel_button, 12, 0)
		
		# Setup
		self.widget = QWidget()
		self.widget.setLayout(self.layout)
		self.main_window.setCentralWidget(self.widget)
		
		# Actions
		self.submit_button.clicked.connect(self.create_patient_submit_button_clicked)
		self.cancel_button.clicked.connect(self.cancel_button_clicked)
	
	# checks if new paitent info is valid and displays error if not valid, goes back to main menu if valid
	def create_patient_submit_button_clicked(self):
		phn = self.text_phn.text()
		name = self.text_name.text()
		birthdate = self.text_birthdate.text()
		phone = self.text_phone.text()
		email = self.text_email.text()
		address = self.text_address.text()
		
		try:
			self.controller.create_patient(phn, name, birthdate, phone, email, address)
			QMessageBox.information(self.main_window, "Operation Success", "Patient created")
			self.main_menu()
		except IllegalAccessException:
			QMessageBox.warning(self.main_window, "Illegal Access", " Cannot perform operations while not logged in")
		except IllegalOperationException:
			self.text_phn.setText("")
			self.text_name.setText("")
			self.text_birthdate.setText("")
			self.text_phone.setText("")
			self.text_email.setText("")
			self.text_address.setText("")
			QMessageBox.warning(self.main_window, "Illegal Operation", "Could not create patient")
	
	# displays field for search patient by phn
	def search_patient_button_clicked(self):
		# Clear window and set layout
		self.main_window.setCentralWidget(None)
		self.layout = QGridLayout()
		self.main_window.resize(300, 400)

		# Data input and labels
		self.label_phn = QLabel("PHN:")
		self.text_phn = QLineEdit()
		self.label_output = QLabel("")
		
		# Buttons
		self.submit_button = QPushButton("Search Patient")
		self.cancel_button = QPushButton("Cancel")
		
		# Adding Widgets
		self.layout.addWidget(self.label_phn, 0, 0)
		self.layout.addWidget(self.text_phn, 0, 1)
		
		self.layout.addWidget(self.submit_button, 1, 1)
		self.layout.addWidget(self.cancel_button, 1, 0)
		
		self.layout.addWidget(self.label_output, 3, 1) # change to qlabels and field text not editable
		
		# Setup
		self.widget = QWidget()
		self.widget.setLayout(self.layout)
		self.main_window.setCentralWidget(self.widget)
		
		# Actions
		self.submit_button.clicked.connect(self.search_patient_submit_button_clicked)
		self.cancel_button.clicked.connect(self.cancel_button_clicked)
	
	# checks if patient search  comes back valid or not
	def search_patient_submit_button_clicked(self):
		phn = self.text_phn.text()
		try:
			patient = self.controller.search_patient(phn)
			self.label_output.setText("PHN: {}\nName: {}\nBirthdate: {}\nPhone: {}\nEmail: {}\nAddress: {}".format(patient.phn, patient.name, patient.birth_date, patient.phone, patient.email, patient.address))
			self.main_window.resize(self.layout.sizeHint().width(), 400)
		except AttributeError:
			self.text_phn.setText("")
			self.label_output.setText("")
			QMessageBox.warning(self.main_window, "Illegal Operation", "Patient doesn't exist")

		except IllegalAccessException:
			self.text_phn.setText("")
			self.label_output.setText("")
			QMessageBox.warning(self.main_window, "Illegal Access", " Cannot perform operations while not logged in")
	
	# displays field for searching by patient name
	def search_patient_name_button_clicked(self):
		# Clear window and set layout
		self.main_window.setCentralWidget(None)
		self.layout = QGridLayout()
		self.main_window.resize(750, 500)
		
		# Data input and labels
		self.label_text = QLabel("Search by name:")
		self.text_text = QLineEdit()
		self.display = QTableView()
		
		
		# Buttons
		self.submit_button = QPushButton("Retrieve Patients")
		self.cancel_button = QPushButton("Cancel")
		
		# Adding Widgets
		self.layout.addWidget(self.label_text, 0, 0)
		self.layout.addWidget(self.text_text, 1, 0)
		self.layout.addWidget(self.display, 3, 0)
		
		self.layout.addWidget(self.submit_button, 2, 0)
		self.layout.addWidget(self.cancel_button, 2, 1)
		
		# Setup
		self.widget = QWidget()
		self.widget.setLayout(self.layout)
		self.main_window.setCentralWidget(self.widget)
		
		# Actions
		self.submit_button.clicked.connect(self.search_patient_name_submit_button_clicked)
		self.cancel_button.clicked.connect(self.cancel_button_clicked)
	
	# searches for patients with name fitting the criteria and displays it in a QTableView
	def search_patient_name_submit_button_clicked(self):
		self.display.clearSpans()
		text = self.text_text.text()
		
		try:
			record = self.controller.retrieve_patients(text)
			model = QStandardItemModel()
			model.setHorizontalHeaderLabels(["PHN", "Name", "Birthdate", "Phone", "Email", "Address"])
			for person in record:
				row = []
				phn_item = QStandardItem(person.phn)
				name_item = QStandardItem(person.name)
				birthdate_item = QStandardItem(person.birth_date)
				phone_item = QStandardItem(person.phone)
				email_item = QStandardItem(person.email)
				address_item = QStandardItem(person.address)
				
				phn_item.setEditable(False)
				name_item.setEditable(False)
				birthdate_item.setEditable(False)
				phone_item.setEditable(False)
				email_item.setEditable(False)
				address_item.setEditable(False)
				
				row.append(phn_item)
				row.append(name_item)
				row.append(birthdate_item)
				row.append(phone_item)
				row.append(email_item)
				row.append(address_item)
				model.appendRow(row)
			self.display.setModel(model)
			
			self.display.resizeColumnsToContents()
			self.display.resizeRowsToContents()
	
		except IllegalAccessException:
			QMessageBox.warning(self.main_window, "Illegal Access", " Cannot perform operations while not logged in")
	
	# displays fields for updating patients info
	def update_patient_button_clicked(self):
		# Clear window and set layout
		self.main_window.setCentralWidget(None)
		self.layout = QGridLayout()

		# Data input and labels
		self.label_oldphn = QLabel("Search PHN:")
		self.text_oldphn = QLineEdit()
		self.label_newphn = QLabel("New PHN:")
		self.text_newphn = QLineEdit()
		self.label_name = QLabel("Name:")
		self.text_name = QLineEdit()
		self.label_birthdate = QLabel("Birth Date:")
		self.text_birthdate = QLineEdit()
		self.label_phone = QLabel("Phone:")
		self.text_phone = QLineEdit()
		self.label_email = QLabel("Email:")
		self.text_email = QLineEdit()
		self.label_address = QLabel("Address:")
		self.text_address = QLineEdit()
		
		# Buttons
		self.submit_button = QPushButton("Update Patient")
		self.cancel_button = QPushButton("Cancel")
		
		# Adding Widgets
		self.layout.addWidget(self.label_oldphn, 0, 0)
		self.layout.addWidget(self.text_oldphn, 0, 1)
		self.layout.addWidget(self.label_newphn, 1, 0)
		self.layout.addWidget(self.text_newphn, 1, 1)
		self.layout.addWidget(self.label_name, 2, 0)
		self.layout.addWidget(self.text_name, 2, 1)
		self.layout.addWidget(self.label_birthdate, 3, 0)
		self.layout.addWidget(self.text_birthdate, 3, 1)
		self.layout.addWidget(self.label_phone, 4, 0)
		self.layout.addWidget(self.text_phone, 4, 1)
		self.layout.addWidget(self.label_email, 5, 0)
		self.layout.addWidget(self.text_email, 5, 1)
		self.layout.addWidget(self.label_address, 6, 0)
		self.layout.addWidget(self.text_address, 6, 1)
		
		self.layout.addWidget(self.submit_button, 7, 1)
		self.layout.addWidget(self.cancel_button, 7, 0)
		
		# Setup
		self.widget = QWidget()
		self.widget.setLayout(self.layout)
		self.main_window.setCentralWidget(self.widget)
		
		# Actions
		self.submit_button.clicked.connect(self.update_patient_submit_button_clicked)
		self.cancel_button.clicked.connect(self.cancel_button_clicked)
	
	# checks if phn is used for patient and updates patient if they exist
	def update_patient_submit_button_clicked(self):
		oldphn = self.text_oldphn.text()
		newphn = self.text_newphn.text()
		name = self.text_name.text()
		birthdate = self.text_birthdate.text()
		phone = self.text_phone.text()
		email = self.text_email.text()
		address = self.text_address.text()
		
		try:
			self.controller.update_patient(oldphn, newphn, name, birthdate, phone, email, address)
			QMessageBox.information(self.main_window, "Operation Success", "Patient updated")
			self.main_menu()
		except IllegalAccessException:
			QMessageBox.warning(self.main_window, "Illegal Access", " Cannot perform operations while not logged in")
		except IllegalOperationException:
			self.text_oldphn.setText("")
			self.text_newphn.setText("")
			self.text_name.setText("")
			self.text_birthdate.setText("")
			self.text_phone.setText("")
			self.text_email.setText("")
			self.text_address.setText("")
			QMessageBox.warning(self.main_window, "Illegal Operation", "Could not update patient")
		
	# displays fields for deleting a paitent
	def delete_patient_button_clicked(self):
		# Clear window and set layout
		self.main_window.setCentralWidget(None)
		self.layout = QGridLayout()

		# Data input and labels
		self.label_phn = QLabel("PHN:")
		self.text_phn = QLineEdit()
		
		# Buttons
		self.submit_button = QPushButton("Delete Patient")
		self.cancel_button = QPushButton("Cancel")
		
		# Adding Widgets
		self.layout.addWidget(self.label_phn, 0, 0)
		self.layout.addWidget(self.text_phn, 0, 1)
		
		self.layout.addWidget(self.submit_button, 1, 1)
		self.layout.addWidget(self.cancel_button, 1, 0)
		
		# Setup
		self.widget = QWidget()
		self.widget.setLayout(self.layout)
		self.main_window.setCentralWidget(self.widget)
		
		# Actions
		self.submit_button.clicked.connect(self.delete_patient_submit_button_clicked)
		self.cancel_button.clicked.connect(self.cancel_button_clicked)
		
	# deletes patient if given phn exists, displays error if patient doesn't exist
	def delete_patient_submit_button_clicked(self):
		phn = self.text_phn.text()
		try:
			patient = self.controller.delete_patient(phn)
			QMessageBox.information(self.main_window, "Operation Success", "Patient deleted")
			self.main_menu()
		
		except IllegalOperationException:
			self.text_phn.setText("")
			QMessageBox.warning(self.main_window, "Illegal Operation", "Patient doesn't exist")

		except IllegalAccessException:
			
			QMessageBox.warning(self.main_window, "Illegal Access", " Cannot perform operations while not logged in")

	# displays field for listing all patients in QTableView
	def list_all_patients_button_clicked(self):
		# Clear window and set layout
		self.main_window.setCentralWidget(None)
		self.layout = QGridLayout()
		self.main_window.resize(750, 500)
		
		# Data input and labels
		self.display = QTableView()
		
		# Buttons
		self.submit_button = QPushButton("List Patients")
		self.cancel_button = QPushButton("Cancel")
		
		# Adding Widgets
		self.layout.addWidget(self.display, 3, 0)
		
		self.layout.addWidget(self.submit_button, 2, 0)
		self.layout.addWidget(self.cancel_button, 2, 1)
		
		# Setup
		self.widget = QWidget()
		self.widget.setLayout(self.layout)
		self.main_window.setCentralWidget(self.widget)
		
		# Actions
		self.submit_button.clicked.connect(self.list_all_patients_submit_button_clicked)
		self.cancel_button.clicked.connect(self.cancel_button_clicked)
	
	# lists all patients if patients are in system
	def list_all_patients_submit_button_clicked(self):
		self.display.clearSpans()
		try:
			record = self.controller.list_patients()
			
			model = QStandardItemModel()
			model.setHorizontalHeaderLabels(["PHN", "Name", "Birthdate", "Phone", "Email", "Address"])
			for person in record:
				row = []
				phn_item = QStandardItem(person.phn)
				name_item = QStandardItem(person.name)
				birthdate_item = QStandardItem(person.birth_date)
				phone_item = QStandardItem(person.phone)
				email_item = QStandardItem(person.email)
				address_item = QStandardItem(person.address)
				
				phn_item.setEditable(False)
				name_item.setEditable(False)
				birthdate_item.setEditable(False)
				phone_item.setEditable(False)
				email_item.setEditable(False)
				address_item.setEditable(False)
				
				row.append(phn_item)
				row.append(name_item)
				row.append(birthdate_item)
				row.append(phone_item)
				row.append(email_item)
				row.append(address_item)
				model.appendRow(row)
			self.display.setModel(model)
			
			self.display.resizeColumnsToContents()
			self.display.resizeRowsToContents()

		except IllegalAccessException:
			QMessageBox.warning(self.main_window, "Illegal Access", " Cannot perform operations while not logged in")

	# displays field for phn for user to enter current patient
	def start_appointment_button_clicked(self):
		# Clear window and set layout
		self.main_window.setCentralWidget(None)
		self.layout = QGridLayout()

		# Data input and labels
		self.label_phn = QLabel("PHN:")
		self.text_phn = QLineEdit()
		
		# Buttons
		self.submit_button = QPushButton("Start Appointment")
		self.cancel_button = QPushButton("Cancel")
		
		# Adding Widgets
		self.layout.addWidget(self.label_phn, 0, 0)
		self.layout.addWidget(self.text_phn, 0, 1)
		
		self.layout.addWidget(self.submit_button, 1, 1)
		self.layout.addWidget(self.cancel_button, 1, 0)
		
		# Setup
		self.widget = QWidget()
		self.widget.setLayout(self.layout)
		self.main_window.setCentralWidget(self.widget)
		
		# Actions
		self.submit_button.clicked.connect(self.start_appointment_submit_button_clicked)
		self.cancel_button.clicked.connect(self.cancel_button_clicked)
		
	# checks if given phn exists and starts appointment if patient is in system
	def start_appointment_submit_button_clicked(self):
		phn = self.text_phn.text()
		try:
			patient = self.controller.set_current_patient(phn)
			self.appointment_menu_gui.appointment_menu()
		
		except IllegalOperationException:
			self.text_phn.setText("")
			QMessageBox.warning(self.main_window, "Illegal Operation", "Patient doesn't exist")

		except IllegalAccessException:
			self.text_phn.setText("")
			QMessageBox.warning(self.main_window, "Illegal Access", " Cannot perform operations while not logged in")

	# when log out button clicked, logs user out and goes back to log in menu
	def log_out_button_clicked(self):
		try:
			self.controller.logout()
			self.main_window.display_login()
			QMessageBox.information(self.main_window, "Operation Success", "Logged out")
		except InvalidLogoutException:
			QMessageBox.warning(self.main_window, "Illegal Operation", "Could not log out")
			
	
	# returns to main menu when cancel button clicked
	def cancel_button_clicked(self):
		self.main_menu()

		
