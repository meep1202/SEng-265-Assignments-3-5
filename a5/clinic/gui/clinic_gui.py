import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout
from clinic.controller import Controller
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.gui.main_menu_gui import MainMenuGUI

class ClinicGUI(QMainWindow):

	def __init__(self):
		super().__init__()
		# Continue here with your code!
		self.controller = Controller(autosave=True)
		self.main_menu_gui = MainMenuGUI(self, self.controller)
		self.setWindowTitle("Clinic")
		self.setMinimumSize(100, 100)
		self.widget = None
		self.layout = None
		
		self.display_login()


	# displays log in menu
	def display_login(self):
		self.resize(250, 150)
		self.setCentralWidget(None)
		self.layout = QGridLayout()
		

		label_username = QLabel("Username")
		self.text_username = QLineEdit()
		label_password = QLabel("Password")
		self.text_password = QLineEdit()
		self.text_password.setEchoMode(QLineEdit.EchoMode.Password)
		self.button_login = QPushButton("Login")
		self.button_quit = QPushButton("Quit")

		self.layout.addWidget(label_username, 0, 0)
		self.layout.addWidget(self.text_username, 0, 1)
		self.layout.addWidget(label_password, 1, 0)
		self.layout.addWidget(self.text_password, 1, 1)
		self.layout.addWidget(self.button_login, 2, 1)
		self.layout.addWidget(self.button_quit, 2, 0)

		self.widget = QWidget()
		self.widget.setLayout(self.layout)
		self.setCentralWidget(self.widget)
		
		
		
		self.button_login.clicked.connect(self.login_button_clicked)
		self.button_quit.clicked.connect(self.quit_button_clicked)
		
	# controls what login button does when clicked
	def login_button_clicked(self):

		username = self.text_username.text()
		password = self.text_password.text()
		
		try:
			self.controller.login(username, password)
			
			self.main_menu_gui.main_menu()
			
		except InvalidLoginException:
			QMessageBox.warning(self, "Log in Failed", "Log in was not successful")
			self.text_username.setText("")
			self.text_password.setText("")
			
	
	# controls quit button
	def quit_button_clicked(self):
		
		self.close()

def main():
	app = QApplication(sys.argv)
	window = ClinicGUI()
	window.show()
	app.exec()

if __name__ == '__main__':
	main()
