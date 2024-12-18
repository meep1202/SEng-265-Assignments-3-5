from clinic.controller import Controller
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout, QPlainTextEdit

class AppointmentMenuGUI():

	def __init__(self, main_menu, main_window, controller):
		self.main_menu = main_menu
		self.controller = controller
		self.main_window = main_window
		
	# displays appointment menu for different actions that can be done
	def appointment_menu(self):
		# Clear window and set layout
		self.main_window.setCentralWidget(None)
		self.layout = QGridLayout()
		
		# Data input and labels
		self.create_note = QPushButton("Create New Note")
		self.retrieve_notes = QPushButton("Retrieve Existing Notes by Text")
		self.update_note = QPushButton("Update Existing Note")
		self.delete_note = QPushButton("Delete Existing Note")
		self.list_record = QPushButton("List Patient Record")
		self.end_appointment = QPushButton("End Appointment")
		
		# Adding Widgets
		self.layout.addWidget(self.create_note, 0, 0)
		self.layout.addWidget(self.retrieve_notes, 1, 0)
		self.layout.addWidget(self.update_note, 2, 0)
		self.layout.addWidget(self.delete_note, 3, 0)
		self.layout.addWidget(self.list_record, 4, 0)
		self.layout.addWidget(self.end_appointment, 5, 0)
		
		# Setup
		self.widget = QWidget()
		self.widget.setLayout(self.layout)
		self.main_window.setCentralWidget(self.widget)
		
		# Actions
		self.create_note.clicked.connect(self.create_note_button_clicked)
		self.retrieve_notes.clicked.connect(self.retrieve_notes_button_clicked)
		self.update_note.clicked.connect(self.update_note_button_clicked)
		self.delete_note.clicked.connect(self.delete_note_button_clicked)
		self.list_record.clicked.connect(self.list_record_button_clicked)
		self.end_appointment.clicked.connect(self.end_appointment_button_clicked)
	
	# displays fields for creating a new note for current patient
	def create_note_button_clicked(self):
		# Clear window and set layout
		self.main_window.setCentralWidget(None)
		self.layout = QGridLayout()
		
		# Data input and labels
		self.label_text = QLabel("Note Text:")
		self.text_text = QLineEdit()
		
		# Buttons
		self.submit_button = QPushButton("Create Note")
		self.cancel_button = QPushButton("Cancel")
		
		# Adding Widgets
		self.layout.addWidget(self.label_text, 0, 0)
		self.layout.addWidget(self.text_text, 0, 1)
		
		self.layout.addWidget(self.submit_button, 1, 1)
		self.layout.addWidget(self.cancel_button, 1, 0)
		
		# Setup
		self.widget = QWidget()
		self.widget.setLayout(self.layout)
		self.main_window.setCentralWidget(self.widget)
		
		# Actions
		self.submit_button.clicked.connect(self.create_note_submit_button_clicked)
		self.cancel_button.clicked.connect(self.cancel_button_clicked)
	
	# creates new note and returns to appointmentmenu
	def create_note_submit_button_clicked(self):
		text = self.text_text.text()

		try:
			note = self.controller.create_note(text)
			QMessageBox.information(self.main_window, "Operation Success", "Note created. \nNote Code: " + str(note.code))
			self.appointment_menu()
		except IllegalAccessException:
			QMessageBox.warning(self.main_window, "Illegal Access", " Cannot perform operations while not logged in")
		except NoCurrentPatientException:
			QMessageBox.warning(self.main_window, "Illegal Operation", "No current patient active")

	# displays fields for search for notes with keywords
	def retrieve_notes_button_clicked(self):
		# Clear window and set layout
		self.main_window.setCentralWidget(None)
		self.layout = QGridLayout()
		
		# Data input and labels
		self.label_text = QLabel("Search by text:")
		self.text_text = QLineEdit()
		self.display = QPlainTextEdit()
		
		# Buttons
		self.submit_button = QPushButton("Retrieve Notes")
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
		self.submit_button.clicked.connect(self.retrieve_notes_submit_button_clicked)
		self.cancel_button.clicked.connect(self.cancel_button_clicked)
	
	# searches for notes with given keyword and displays the notes
	def retrieve_notes_submit_button_clicked(self):
		self.display.clear()
		text = self.text_text.text()
		try:
			record = self.controller.retrieve_notes(text)
			for note in record:
				self.display.appendPlainText(str(note.code) + ": " + note.text)
		
		except TypeError:
			self.text_text.setText("")
			QMessageBox.warning(self.main_window, "Illegal Operation", "Cannot list empty record")
		
		except IllegalAccessException:
			QMessageBox.warning(self.main_window, "Illegal Access", "Cannot perform operations while not logged in")
		except NoCurrentPatientException:
			QMessageBox.warning(self.main_window, "Illegal Operation", "No current patient active")

	# displays fields for updating notes
	def update_note_button_clicked(self):
		# Clear window and set layout
		self.main_window.setCentralWidget(None)
		self.layout = QGridLayout()
		
		# Data input and labels
		self.label_code = QLabel("Code:")
		self.text_code = QLineEdit()
		self.label_text = QLabel("Note Text:")
		self.text_text = QLineEdit()
		
		# Buttons
		self.submit_button = QPushButton("Update Note")
		self.cancel_button = QPushButton("Cancel")
		
		# Adding Widgets
		self.layout.addWidget(self.label_code, 0, 0)
		self.layout.addWidget(self.text_code, 0, 1)
		self.layout.addWidget(self.label_text, 1, 0)
		self.layout.addWidget(self.text_text, 1, 1)
		
		self.layout.addWidget(self.submit_button, 2, 1)
		self.layout.addWidget(self.cancel_button, 2, 0)
		
		# Setup
		self.widget = QWidget()
		self.widget.setLayout(self.layout)
		self.main_window.setCentralWidget(self.widget)
		
		# Actions
		self.submit_button.clicked.connect(self.update_note_submit_button_clicked)
		self.cancel_button.clicked.connect(self.cancel_button_clicked)
	
	# updates note if given note code exists
	def update_note_submit_button_clicked(self):
		
		
		try:
			code = int(self.text_code.text())
			text = self.text_text.text()
			if self.controller.update_note(code, text):
				QMessageBox.information(self.main_window, "Operation Success", "Note updated")
				self.appointment_menu()
			else:
				self.text_code.setText("")
				self.text_text.setText("")
				QMessageBox.warning(self.main_window, "Illegal Operation", "Code has to be a valid number")
		except ValueError:
			self.text_code.setText("")
			self.text_text.setText("")
			QMessageBox.warning(self.main_window, "Illegal Operation", "Code has to be a number")
		except IllegalAccessException:
			QMessageBox.warning(self.main_window, "Illegal Access", " Cannot perform operations while not logged in")
		except NoCurrentPatientException:
			QMessageBox.warning(self.main_window, "Illegal Operation", "No current patient active")

	# displays field for deleting a note by key
	def delete_note_button_clicked(self):
		# Clear window and set layout
		self.main_window.setCentralWidget(None)
		self.layout = QGridLayout()
		
		# Data input and labels
		self.label_code = QLabel("Code:")
		self.text_code = QLineEdit()
		
		# Buttons
		self.submit_button = QPushButton("Delete Note")
		self.cancel_button = QPushButton("Cancel")
		
		# Adding Widgets
		self.layout.addWidget(self.label_code, 0, 0)
		self.layout.addWidget(self.text_code, 0, 1)
		
		self.layout.addWidget(self.submit_button, 1, 1)
		self.layout.addWidget(self.cancel_button, 1, 0)
		
		# Setup
		self.widget = QWidget()
		self.widget.setLayout(self.layout)
		self.main_window.setCentralWidget(self.widget)
		
		# Actions
		self.submit_button.clicked.connect(self.delete_note_submit_button_clicked)
		self.cancel_button.clicked.connect(self.cancel_button_clicked)

	# deletes note if given key exists
	def delete_note_submit_button_clicked(self):
		
		
		try:
			code = int(self.text_code.text())
			if self.controller.delete_note(code):
				QMessageBox.information(self.main_window, "Operation Success", "Note deleted")
				self.appointment_menu()
			else:
				self.text_code.setText("")
				QMessageBox.warning(self.main_window, "Illegal Operation", "Code has to be a valid number")
		except ValueError:
			self.text_code.setText("")
			QMessageBox.warning(self.main_window, "Illegal Operation", "Code has to be a number")
		except IllegalAccessException:
			QMessageBox.warning(self.main_window, "Illegal Access", " Cannot perform operations while not logged in")
		except NoCurrentPatientException:
			QMessageBox.warning(self.main_window, "Illegal Operation", "No current patient active")

	#displays fields for listing all of a patients notes
	def list_record_button_clicked(self):
		# Clear window and set layout
		self.main_window.setCentralWidget(None)
		self.layout = QGridLayout()
		
		# Data input and labels
		self.display = QPlainTextEdit()
		
		# Buttons
		self.submit_button = QPushButton("List Notes")
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
		self.submit_button.clicked.connect(self.list_record_submit_button_clicked)
		self.cancel_button.clicked.connect(self.cancel_button_clicked)

	# displays all given notes of a patients
	def list_record_submit_button_clicked(self):
		self.display.clear()
		try:
			record = self.controller.list_notes()
			for note in record:
				self.display.appendPlainText(str(note.code) + ": " + note.text)
				
		except IllegalAccessException:
			QMessageBox.warning(self.main_window, "Illegal Access", " Cannot perform operations while not logged in")
		except NoCurrentPatientException:
			QMessageBox.warning(self.main_window, "Illegal Operation", "No current patient active")

	# ends appointment and returns to clinic main menu
	def end_appointment_button_clicked(self):
		try:
			self.controller.unset_current_patient()
			self.main_menu.main_menu()
			QMessageBox.information(self.main_window, "Operation Success", "Appointment Complete")

		except IllegalAccessException:
			QMessageBox.warning(self.main_window, "Illegal Access", "Cannot perform operations while not logged in")

	# returns to appointment menu
	def cancel_button_clicked(self):
		self.appointment_menu()








