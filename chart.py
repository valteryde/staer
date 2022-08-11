
import os
from .id import getid


class Chart:
    def __init__(self):
        pass

    def head(self):
        return ''


class LineChart(Chart):
    def __init__(self, title, cb, size:tuple=(2,2)):
        super(LineChart, self).__init__()
        absPath = os.path.dirname(__file__)
        self.id =  'ch' + getid()
        self.html = open(os.path.join(absPath, 'component', 'linechart.html'), 'r').read()
        self.html = self.html.replace('{title}', title)
        self.html = self.html.replace('{id}', self.id)
        self.cb = cb

        self.html = self.html.replace('{width}', str(size[0]))
        self.html = self.html.replace('{height}', str(size[1]))


    def body(self):
        x, y = self.cb()
        html = self.html.replace('{x}', str(x))
        html = html.replace('{y}', str(y))
        return html


class PieChart(Chart):
    def __init__(self, title, cb, size=(1,1)):
        super(PieChart, self).__init__()
        absPath = os.path.dirname(__file__)
        self.id =  'ch' + getid()
        self.html = open(os.path.join(absPath, 'component', 'piechart.html'), 'r').read()
        self.html = self.html.replace('{title}', title)
        self.html = self.html.replace('{id}', self.id)
        self.cb = cb

        self.html = self.html.replace('{width}', str(size[0]))
        self.html = self.html.replace('{height}', str(size[1]))


    def body(self):
        label, val = self.cb()
        html = self.html.replace('{label}', str(label))
        html = html.replace('{val}', str(val))
        return html
