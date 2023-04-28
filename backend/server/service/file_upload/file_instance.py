class file_instance:
    
    def __init__(self, file):
        self.file = file
        
    @property
    def getFile(self):
        return self.file
    
    @getFile.setter
    def setFile(self, file):
        self.file = file