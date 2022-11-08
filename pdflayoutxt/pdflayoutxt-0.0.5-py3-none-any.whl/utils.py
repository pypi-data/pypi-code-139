
class InvalidFileFormat(Exception):
    
    def __init__(self, value,key):
        self.value = value
        self.key =key
        
    def __str__(self):
        return f"{self.key} is invalid input, get_text function can only accept a '.pdf' or '.PDF' file format."
    
    
class InvalidPageNumbers(Exception):
    
    def __init__(self, value,key):
        self.value = value
        self.key =key
        
    def __str__(self):
        return f"{self.key} is invalid input of page numbers, get_text functions, Pages argument can only be a list like [1,2,3,4] or an integer like 5."