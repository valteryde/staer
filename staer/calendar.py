
import os

import flask
from .id import getid
from .admin import routes, adminList
import datetime


class Calendar:
    def __init__(self, title, get, delete, size:tuple=(2,3)):
        self.title = title
        self.get = get
        self.delete = delete
    
        absPath = os.path.dirname(__file__)
        self.html = open(os.path.join(absPath, 'component', 'calendar.html'), 'r').read()
        self.id = getid()
        self.html = self.html.replace('{id}', self.id)
        self.html = self.html.replace('{title}', title)
        self.html = self.html.replace('{width}', str(size[0]))
        self.html = self.html.replace('{height}', str(size[1]))
        
        self.datesep = '-'

        routes.append(('/admin/calendar/{}/get'.format(self.id), self.getView))
        routes.append(('/admin/calendar/{}/delete'.format(self.id), self.deleteView))

    
    # routes
    def getView(self):
        adminList[0].verify()
        year = flask.request.args.get('year')
        month = flask.request.args.get('month')

        return flask.jsonify(self.get(year, month))


    def deleteView(self):
        adminList[0].verify()
        id = flask.request.args.get('timeid')
        resp = self.delete(id)
        if resp == True:
            return '', 200
        else:
            return resp, 400


    def changeMonth(self, data:list[list[str]]) -> list:
        
        for i, d in enumerate(data):

            start = d[1].split(self.datesep)
            start[1] = str(int(start[1]) - 1)
            start = self.datesep.join(start)
            end = d[2].split(self.datesep)
            end[1] = str(int(end[1]) - 1)
            end = self.datesep.join(end)
            
            data[i][1] = start
            data[i][2] = end

        return data


    def body(self):
        today = datetime.date.today()
        return self.html.replace('{times}', str(self.changeMonth(self.get(today.year,today.month))))


    def head(self):
        return ''


    def rule(self):
        pass