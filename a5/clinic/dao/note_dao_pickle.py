from clinic.dao.note_dao import NoteDAO
from clinic.note import Note
from pickle import dump, load

class NoteDAOPickle(NoteDAO):
    # NoteDAOPickle initialization
    def __init__(self, phn, autosave=True):
        self.autosave = autosave
        self.phn = phn
        self.autocounter = 1
        self.notes = []
        self.filename = "clinic/records/" + str(self.phn) + ".dat"
        if (self.autosave):
            self.read_patient_note()
                
    # reads and saves a patients notes file
    def read_patient_note(self):
        self.notes = []
        try:
            with open(self.filename, 'rb') as file:
                while True:
                    try:
                        self.notes.append(load(file))
                    except EOFError:
                        break
            file.close()
            if len(self.notes) > 0:
                self.autocounter = self.notes[-1].code + 1
            else:
                self.autocounter = 1
        except FileNotFoundError:
            file = open(self.filename, 'x')
            file.close()
            self.autocounter = 1
        
    # writes a patients notes to file
    def write_patient_notes(self):
        with open(self.filename, 'wb') as file:
            for cur_note in self.notes:
                dump(cur_note, file)
        file.close()
    
    # searches for a patients note by given key value
    def search_note(self, key):
        for i in range(len(self.notes)):
            if (key == self.notes[i].code):
                return self.notes[i]
        return None

    # creates a new patients note
    def create_note(self, text):
        self.notes.append(Note(self.autocounter, text))
        self.autocounter += 1
        if (self.autosave):
            self.write_patient_notes()
        return self.notes[-1]

    # searches for a note with given word or string
    def retrieve_notes(self, search_string):
        notes_containing = []
        for i in range(len(self.notes)):
            if self.notes[i].search_keyword_in_text(search_string) is True:
                notes_containing.append(self.notes[i])
        return notes_containing

    # updates a patients note with new text, writes to file if autosave is True
    def update_note(self, key, text):
        for i in range(len(self.notes)):
            if (key == self.notes[i].code):
                self.notes[i].update_text(text)
                if (self.autosave):
                    self.write_patient_notes()
                return True
        return False

    # deletes a patients note, updates patients note file if autosave is True
    def delete_note(self, key):
        for i in range(len(self.notes)):
            if (key == self.notes[i].code):
                self.notes.pop(i)
                if (self.autosave):
                    self.write_patient_notes()
                return True
        return False

    # returns a list of the current patients notes
    def list_notes(self):
        notes_in_order = []
        for i in range(len(self.notes)-1, -1, -1):
            notes_in_order.append(self.notes[i])
        return notes_in_order
