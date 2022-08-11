
import os
from .id import getid
from .admin import adminList, routes
from .api import ApiHandler
import flask


class Table:
    def __init__(self, title:str, colNames:list[str], data:tuple, tablename:str='', editable:bool=False, searchable:bool=False, deletable:bool=False, size:tuple=(3,2)):
        absPath = os.path.dirname(__file__)
        self.tablenumber = getid()
        self.tablename = tablename
        self.html = open(os.path.join(absPath, 'component', 'table.html'), 'r').read().replace('{id}', 'tb{}'.format(self.tablenumber))

        self.html = self.html.replace('{width}', str(size[0]))
        self.html = self.html.replace('{height}', str(size[1]))

        if editable:
            self.html = self.html.replace('{button}', '<button class="table-create-new"><span class="material-symbols-outlined">add</span></button>')
        else:
            self.html = self.html.replace('{button}', '')

        if searchable:
            self.html = self.html.replace('{search}', '<input onkeydown="tb{}.fetch(this.value)" class="table-input-search" type="text" placeholder="Søg">'.format(self.tablenumber))
        else:
            self.html = self.html.replace('{search}', '')

        self.cols = [i[1] for i in colNames]
        self.types = []
        for i in colNames:
            if len(i) > 2:
                self.types.append(i[2])
            else:
                self.types.append("null")
            
        # add header
        html = ''
        for cn in colNames:
            cn = cn[0]
            html += '<th>{}</th>'.format(cn)

        if deletable:
            html += '<th>&nbsp;&nbsp;</th>'
        self.delete = deletable
        self.edit = editable

        self.html = self.html.replace('{header}', html)
        self.html = self.html.replace('{title}', title)

        # handle api
        self.url = '/admin/table/api/{}'.format(self.tablenumber)

        self.api = data
        routes.append((self.url, self.apiview, ['GET']))
        self.handler = ApiHandler()


    def apiview(self):
        adminList[0].verify()
        return flask.jsonify(self.api(*self.handler.parse(flask.request)))


    def head(self):
        return '<script defer>const tb{} = new Table(`tb{}` ,`{}`, `{}`, {}, {}, {delete}, {edit});tb{}.fetch()</script>'.format(
            self.tablenumber, 
            self.tablenumber, 
            self.url, 
            self.tablename, 
            str(self.cols), 
            str(self.types),
            self.tablenumber, 
            delete = int(self.delete), 
            edit=int(self.edit)
        )

    def body(self):
        return self.html
