from .patient_record import *

class Patient:
    
    # patient initialization
    def __init__(self, phn, name, birth_date, phone, email, address, autosave=True):
        self.phn = phn
        self.name = name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.address = address
        self.autosave = autosave
        self.record = PatientRecord(self.phn, self.autosave)
        
    # patient equal function
    def __eq__(self, other):
        if (self.phn != other.phn):
            return False
        if (self.name != other.name):
            return False
        if (self.birth_date != other.birth_date):
            return False
        if (self.phone != other.phone):
            return False
        if (self.email != other.email):
            return False
        if (self.address != other.address):
            return False
        
        return True
    
    # patient string representation
    def __str__(self):
        return "Patient: %d, %s, %s, %s, %s, %s" % (self.phn, self.name, self.birth_date, self.phone, self.email, self.address)
    
    # getter
    
    def get_phn(self):
        return self.phn
    
    # Patient Record getters
    
    def create_new_note(self, text):
        return self.record.creates_note(text)
        
    def get_one_note(self, note_num):
        return self.record.gets_note(note_num)
    
    def get_all_patient_notes(self):
        return self.record.get_all_notes()
        
    def search_keyword_notes(self, text):
        return self.record.search_keyword(text)
    
    def get_num_patient_notes(self):
        return self.record.get_num_notes()

    def update_patient_note(self, code, text):
        return self.record.update_note(code, text)
        
    def delete_given_note(self, code):
        return self.record.deletes_note(code)
