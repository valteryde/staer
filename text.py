
import os

class Text:
    def __init__(self, title, data=lambda: '', size:tuple=(1,1)):
        absPath = os.path.dirname(__file__)
        self.html = open(os.path.join(absPath, 'component', 'text.html'), 'r').read()
        self.html = self.html.replace('{title}', title)
        self.datafunction = data
        
        self.html = self.html.replace('{width}', str(size[0]))
        self.html = self.html.replace('{height}', str(size[1]))

    def head(self):
        return ''
    
    def body(self):
        return self.html.replace('{dataInsert}',self.datafunction())