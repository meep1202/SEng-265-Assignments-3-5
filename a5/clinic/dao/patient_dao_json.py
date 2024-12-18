from clinic.patient import *
from clinic.dao.patient_dao import PatientDAO
from clinic.dao.patient_decoder import PatientDecoder
from clinic.dao.patient_encoder import PatientEncoder
import json
import os

class PatientDAOJSON(PatientDAO):
    # PatientDAOJSON initialization
    def __init__(self, autosave):
        self.autosave = autosave
        self.filename = "clinic/patients.json"
        self.patients = []
        if self.autosave is True:
            self.decode_to_list()

    # reads patients from file
    def decode_to_list(self):
        try:
            with open(self.filename, 'r') as file:
                if os.path.getsize(self.filename):
                    for line in json.load(file):
                        cur_obj = json.dumps(line)
                        patient = json.loads(cur_obj, cls=PatientDecoder)
                        self.patients.append(patient)
                    
            file.close() 
        except FileNotFoundError:
                file = open(self.filename, 'x')
                file.close()
                
    # saves patients to file
    def encode_from_list(self):
        patient_json = json.dumps(self.patients, cls=PatientEncoder)
        with open(self.filename, 'w') as file:
            file.write(patient_json)
        file.close()

    # searches for a patient, returns None if not found
    def search_patient(self, key):
        for i in range(len(self.patients)):
            if self.patients[i].phn == key:
                return self.patients[i]
        return None

    # creates new paitent
    def create_patient(self, phn, name, birth_date, phone, email, address):
        self.patients.append(Patient(phn, name, birth_date, phone, email, address, self.autosave))
        new_patient = self.patients[-1]
        if self.autosave:
            self.encode_from_list()
        return new_patient

    # searches for patient by name
    def retrieve_patients(self, search_string):
        if len(self.patients) == 0:
            return
        retrieval_list = []
        for i in range(len(self.patients)):
            if search_string in self.patients[i].name:
                retrieval_list.append(self.patients[i])
        return retrieval_list

    # updates patient with new information, updates file if autosave is on
    def update_patient(self, oldphn, newphn, name, birth_date, phone, email, address):
        if len(self.patients) == 0: 
            return False
        self.search_patient(oldphn).name = name
        self.search_patient(oldphn).birth_date = birth_date
        self.search_patient(oldphn).phone = phone
        self.search_patient(oldphn).email = email
        self.search_patient(oldphn).address = address
        self.search_patient(oldphn).phn = newphn
        if (self.autosave):
            self.encode_from_list()
			
        return True

    # deletes patient from list, updates file if autosave is on
    def delete_patient(self, key):
        if len(self.patients) == 0: 
            return False
        for i, o in enumerate(self.patients):
            if o.get_phn() == key:
                self.patients.pop(i)
                if (self.autosave):
                    self.encode_from_list()
                    records_path = 'clinic/records'
                    if os.path.exists(records_path):
                        record_file_path = os.path.join(records_path, str(key) + ".dat")
                        if os.path.isfile(record_file_path):
                            os.remove(record_file_path)
                return True 
        return False

    # returns a list of patient objects
    def list_patients(self):
        return self.patients
