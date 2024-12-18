from datetime import datetime

class Note:

    # Note initialization
    def __init__(self, code, text):
        self.code = code # from autocounter
        self.text = text
        self.timestamp = datetime.now() # from datetime.now()
    
    # Note equals function
    def __eq__(self, other):
        return self.code == other.code and self.text == other.text
        
    def __str__(self):
        return "Note: %d, %s, %s" % (self.code, self.text, self.timestamp)
    # checks if given keyword is in a notes text
    def search_keyword_in_text(self, text):
        if text in self.text:
            return True
        return False
    
    # updates a notes text and updates the timestamp
    def update_text(self, text):
        self.text = text
        self.timestamp = datetime.now()
