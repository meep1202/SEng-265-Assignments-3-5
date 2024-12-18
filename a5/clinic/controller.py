from clinic.dao.patient_dao_json import PatientDAOJSON
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException
import hashlib

class Controller:

    # Base Functions
    def __init__(self, autosave):
        self.status_logged_in = False
        self.current_patient = None
        self.autosave = autosave
        self.patient_dao_json = PatientDAOJSON(self.autosave)


    # Login/out Functions
    
    # log out if logged in
    def logout(self):
        if (self.status_logged_in):
            if self.current_patient is not None:
                self.current_patient = None
            self.status_logged_in = False
            return True 
        raise InvalidLogoutException()
    
    # log in with correct credentials
    def login(self, username, password):
    
        if (self.status_logged_in):
            raise DuplicateLoginException()
        users = {}
        if (self.autosave is False):
            
            users = {"user" : "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92", 
            "ali" : "6394ffec21517605c1b426d43e6fa7eb0cff606ded9c2956821c2c36bfee2810", 
            "kala" : "e5268ad137eec951a48a5e5da52558c7727aaa537c8b308b5e403e6b434e036e"}
            
        else:
            file = open("clinic/users.txt", "r")
            for line in file:
                cur_line = line.strip().split(",")
                users[cur_line[0]] = cur_line[1]
            file.close()
            
        encoded_password = password.encode('utf-8')     # Convert the password to bytes
        hash_object = hashlib.sha256(encoded_password)      # Choose a hashing algorithm (e.g., SHA-256)
        hex_dig_password = hash_object.hexdigest()       # Get the hexadecimal digest of the hashed password
    
        if (username in users):
            if (users[username] == hex_dig_password):
                self.status_logged_in = True
                return True
        
        raise InvalidLoginException()


    # Patient functions
    
    # search for patient
    def search_patient(self, phn): 
        if self.status_logged_in is False:
            raise IllegalAccessException()
        return self.patient_dao_json.search_patient(phn)
    
    # create new patient with unique phn
    def create_patient(self, phn, name, birth_date, phone, email, address): 
        if self.status_logged_in is False:
            raise IllegalAccessException()
        if self.patient_dao_json.search_patient(phn) is not None: 
            raise IllegalOperationException()
        return self.patient_dao_json.create_patient(phn, name, birth_date, phone, email, address)
    
    # updates patient info
    def update_patient(self, phn, newphn, name, birth_date, phone, email, address): 
        if self.status_logged_in is False:
            raise IllegalAccessException ()
        if self.current_patient is not None:
            raise IllegalOperationException()
        if self.patient_dao_json.search_patient(phn) is None: 
            raise IllegalOperationException()
        if phn != newphn and self.patient_dao_json.search_patient(newphn) is not None:
            raise IllegalOperationException()
        return self.patient_dao_json.update_patient(phn, newphn, name, birth_date, phone, email, address)
    
    # deletes patient if they exist
    def delete_patient(self, phn): 
        if self.status_logged_in is False:
            raise IllegalAccessException()
        if self.current_patient is not None: 
            raise IllegalOperationException()
        if self.patient_dao_json.search_patient(phn) is None: 
            raise IllegalOperationException()
        return self.patient_dao_json.delete_patient(phn)
        
    # returns a list of all patients
    def list_patients(self): 
        if self.status_logged_in is False:
            raise IllegalAccessException()
        return self.patient_dao_json.list_patients()
    
    # returns list of patients with given name filter
    def retrieve_patients(self, text): 
        if self.status_logged_in is False:
            raise IllegalAccessException()
        return self.patient_dao_json.retrieve_patients(text)
    
    # set current patient to be able to access
    def set_current_patient(self, phn): 
        if self.status_logged_in is False:
            raise IllegalAccessException()
        self.current_patient = self.patient_dao_json.search_patient(phn)
        if self.current_patient is None:
            raise IllegalOperationException()
    
    # return current patient
    def get_current_patient(self): 
        if self.status_logged_in is False:
            raise IllegalAccessException()
        return self.current_patient
    
    # unsets current patient if one is set
    def unset_current_patient(self): 
        if self.status_logged_in is False:
            raise IllegalAccessException()
        self.current_patient = None
        
    
    # PatientRecord/Notes Functions   

    # create new note for current patient
    def create_note(self, text): 
        if self.status_logged_in is False:
            raise IllegalAccessException()
        if self.current_patient is None: 
            raise NoCurrentPatientException()
        return self.current_patient.create_new_note(text)
        
    # searchs current patients notes for note with given code
    def search_note(self, code): 
        if self.status_logged_in is False:
            raise IllegalAccessException()
        if self.current_patient is None: 
            raise NoCurrentPatientException()
        return self.current_patient.get_one_note(code)
    
    # retrieves notes from current patient with given keyword
    def retrieve_notes(self, text): 
        if self.status_logged_in is False:
            raise IllegalAccessException()
        if self.current_patient is None: 
            raise NoCurrentPatientException()
        if self.current_patient.get_num_patient_notes() == 0:
            return None
        
        return self.current_patient.search_keyword_notes(text)
    
    # updates current patients note with the correct code with new text
    def update_note(self, code, text): 
        if self.status_logged_in is False:
            raise IllegalAccessException()
        if self.current_patient is None: 
            raise NoCurrentPatientException()
        return self.current_patient.update_patient_note(code, text)
        
    # deletes the current patients note that has the given code
    def delete_note(self, code): 
        if self.status_logged_in is False:
            raise IllegalAccessException()
        if self.current_patient is None: 
            raise NoCurrentPatientException()
        if self.current_patient.get_num_patient_notes() == 0: 
            return False
            
        return self.current_patient.delete_given_note(code)
    
    # returns a list of all the current patients notes
    def list_notes(self):
        if self.status_logged_in is False:
            raise IllegalAccessException()
        if self.current_patient is None:
            raise NoCurrentPatientException()
        if len(self.patient_dao_json.patients) == 0:
            return None
        
        return self.current_patient.get_all_patient_notes()
