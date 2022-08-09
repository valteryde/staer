
import os
import flask
from .admin import routes, adminList
from .id import getid


class Form:

    class SubTitle:
        def __init__(self, title, text:str=''):
            self.html = '<h3 style="margin:0;margin-top:10px;">{}</h3>'.format(title)
            if text:
                self.html += '<p style="margin:0;margin-bottom:20px;">{}</p>'.format(text)


    class Input:
        def __init__(self, name, placeholder, hidden:bool=False):
            
            tp = 'text'
            if hidden:
                tp = 'password'
            
            self.html = """
            <div class="input-container">
                <input type="{type}" name="{name}" onfocusout="if (this.value.length > 0) {this.classList.add(`notempty`)} else {this.classList.remove(`notempty`)}">
                <p onclick="this.previousElementSibling.focus();">{placeholder}</p>
            </div>
            """.replace('{name}', name).replace('{placeholder}', placeholder).replace('{type}', tp)



    class RadioButtons:
        def __init__(self, name, options, text=None):
            self.html = ''

            if text:
                self.html += '<p style="margin-bottom:0px;">{}</p>'.format(text)
            self.html += '<div class="radio-container" style="grid-template-columns:repeat({}, 1fr)">'.format(str(len(options)))
            
            for id_, nm, graphic in options:
                self.html += '<div onclick="checkRadioButton(this);" class="radio-container-article"> <span class="material-symbols-outlined">{}</span> <p>{}</p>  <input type="radio" name="{}" value="{}"> </div>'.format(graphic, nm, name, id_)

            self.html += '</div>'

    
    class Textarea:
        def __init__(self, name, placeholder):
            
            self.html = """
            <div class="input-container">
                <textarea name="{name}" onfocusout="if (this.innerHTML.length > 0) {this.classList.add(`notempty`)} else {this.classList.remove(`notempty`)}"> </textarea>
                <p onclick="this.previousElementSibling.focus();">{placeholder}</p>
            </div>
            """.replace('{name}', name).replace('{placeholder}', placeholder)

    
    class FileUpload:
        def __init__(self, name):
            self.html = '<div class="input-file-upload" onclick="this.children[0].click()">'
            self.html += '<input name="{name}" type="file" onchange="this.nextElementSibling.nextElementSibling.innerText = `${this.files[0].name}`">'.replace('{name}', name)
            self.html += '<span class="material-symbols-outlined">file_upload</span>'
            self.html += '<p>Upload fil</p>'
            self.html += '</div>'
            self.name = name

    
    # class Checkbox():
    #     def __init__(self):
    #         self.html = ''

    # class ColorPicker():
    #     def __init__(self):
    #         self.html = ''
    
    # class DateInput():
    #     def __init__(self):
    #         self.html = ''
    
    # class Select:
    #     def __init__(self):
    #         self.html = ''



    # form class
    def __init__(self, title, *elements, size:tuple=(1,2), api:str or function=''):
        absPath = os.path.dirname(__file__)
        self.html = open(os.path.join(absPath, 'component', 'form.html'), 'r').read()
        
        self.html = self.html.replace('{width}', str(size[0]))
        self.html = self.html.replace('{height}', str(size[1]))
        self.html = self.html.replace('{title}', title)
        
        self.fileupload = []

        # add elements
        html = ''
        for i in elements:
            if type(i) is Form.FileUpload:
                self.fileupload.append(i.name)
            html += i.html

        self.html = self.html.replace('{elements}', html)

        self.routeID = getid()
        
        # handle api
        self.api = api

        url = '/admin/form/api/{}'.format(self.routeID)

        if callable(api):
            routes.append((url, self.view, ['POST']))
        else:
            url = api

        self.html = self.html.replace('{url}', url)

    
    def view(self):
        adminList[0].verify()
        values = flask.request.form

        if self.fileupload:
            
            temp = {}

            for key in flask.request.files:
                
                file = flask.request.files[key]
                temp[key] = file

            values = temp

        self.api(values)
        return flask.redirect(flask.request.referrer)

    
    def body(self):
        return self.html
    
    
    def head(self):
        return ''
