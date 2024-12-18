from .note import *
from clinic.dao.note_dao_pickle import NoteDAOPickle

class PatientRecord:

    # Patient Record initialization
    def __init__(self, phn=None, autosave=True):
        self.phn = phn
        self.autosave = autosave
        self.note_dao_pickle = NoteDAOPickle(self.phn, self.autosave)
    
    # create new note and add to list of notes
    def creates_note(self, text):
        return self.note_dao_pickle.create_note(text)
    
    # get note with given code
    def gets_note(self, note_num):
        return self.note_dao_pickle.search_note(note_num)
    
    # finds notes containing given keyword(s)   
    def search_keyword(self, text):
        return self.note_dao_pickle.retrieve_notes(text)
    
    # searches for note with given code updates note if note exists with new text
    def update_note(self, code, text):
        return self.note_dao_pickle.update_note(code, text)
    
    # returns all patients notes in order from newest to oldest
    def get_all_notes(self):
        return self.note_dao_pickle.list_notes()
    
    # returns number of notes that a patient has
    def get_num_notes(self):
        return len(self.note_dao_pickle.notes)
    
    # deletes a patients note if note with give code exists
    def deletes_note(self, code):
        return self.note_dao_pickle.delete_note(code)
