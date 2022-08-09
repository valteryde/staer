
import flask
from .form import Form
from .admin import routes, adminList
from .id import getid


class InputBase:
    def __init__(self, get, update):
        self.get = get
        self.update = update

        # handle api
        self.routeID = getid()
        self.url = '/admin/input/api/{}'.format(self.routeID)
        routes.append((self.url, self.view, ['POST']))


    def view(self):
        adminList[0].verify()
        values = flask.request.values
        if type(self) is FileUpload:
            values = flask.request.files
        self.update(values)
        return flask.redirect(flask.request.referrer)


    def body(self):
        return """
            <article class="card c1-1 input-card" data-value="{}">
                <h1>{}</h1>
                <form action="{}" method="post" enctype="multipart/form-data">
                    {} 
                    <input type="submit" value="Gem">
                </form>
                
            </article>
            """.format(
                self.get(),
                self.title, 
                self.url,
                self.html
            )
    def head(self): return ''


class Input(InputBase):
    def __init__(self, get, update, title, name, placeholder, hidden:bool=False):
        super(Input, self).__init__(get, update)
        self.html = Form.Input(name, placeholder, hidden).html
        self.title = title


class RadioButtons(InputBase):
    def __init__(self, get, update, title, name, options):
        super(RadioButtons, self).__init__(get, update)
        self.html = Form.RadioButtons(name, options).html
        self.title = title

    
class Textarea(InputBase):
    def __init__(self, get, update, title, name, placeholder):
        super(Textarea, self).__init__(get, update)
        self.html = Form.Textarea(name, placeholder).html
        self.title = title

    
class FileUpload(InputBase):
    def __init__(self, update, title, name):
        super(FileUpload, self).__init__(lambda:'', update)
        self.html = Form.FileUpload(name).html
        self.title = title
            
        