#import time
from datetime import datetime
from io import BytesIO as StringIO

class Log(object):
    
    def __init__(self):
        self.output = StringIO()
    
    def write(self, text):
        self.output.write(text + '\n')
        
    def writeWithDateTime(self, text):
        d = datetime.now()
        self.write(str(d.strftime("%d-%m-%Y_%I_%M%p")) + ': ' + text)
        
    def toDisk(self, filepath):
        arch = open(filepath, "w")
        arch.write(self.output.getvalue())
        arch.close()