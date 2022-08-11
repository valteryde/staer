
import glob
import random
import flask
import os
import time
import string
from .id import getid

### VIEWS ###
admin = None
adminList = []
routes = []
class AdminHTMLView:
    def __init__(self, html, rules:list=[]):
        self.html = html
        self.rules = rules

    def render(self):

        html = str(self.html)
        for callback, rule in self.rules:
            cres = callback()
            html = html.replace(rule, str(cres))

        return html


    def view(self):
        if not admin.verify():
            return admin.loginRoute()

        return self.render()


### ADMIN ###
class Admin:
    
    def __init__(self, app:flask.Flask, opt, debug:bool=False):
        global admin, routes
        admin = self
        adminList.append(self)

        self.app = app
        self.opt = opt
        self.debug = debug

        # add unmade routes
        for values in routes:
            if len(values) == 2:
                self.app.add_url_rule(values[0], view_func=values[1], endpoint=str(getid()))
            else:
                self.app.add_url_rule(values[0], view_func=values[1], methods=values[2], endpoint=str(getid()))
            
        routes = []

        self.autoLogoutTime = 10 * 60 #seconds

        #self.absPath = os.path.split(os.path.dirname(__file__))
        self.absPath = os.path.dirname(__file__)
        self.template = open(os.path.join(self.absPath,'admin.html'), 'r').read()
        
        # add js and css to template
        html = ''
        for i in glob.glob(os.path.join(self.absPath, 'static', '*.css')):
            html += '<style>' + open(i, 'r').read() + '</style>'
        for i in glob.glob(os.path.join(self.absPath, 'static', '*.js')):
            html += '<script>' + open(i, 'r').read() + '</script>'
        self.template = self.template.replace('{import}', html)

        # add name to template
        self.template = self.template.replace('{logoSRC}', opt["logo"])

        # add page links
        html = ''
        for i in opt["pages"]:
            html += '<article class="sidebar-page" onclick="window.location = `/admin/{}`"><span class="material-symbols-outlined">{}</span></article>'.format(i["name"].replace(' ', ''), i["icon"])

        self.template = self.template.replace('{pageMarks}', html)

        # add colors
        self.template = self.template.replace('{mainColor}', opt["color"])

        # pages
        if opt.get('pages'):
            self.pages = opt["pages"]
            for page in self.pages:
                self.addRule(page)

        if len(opt.get('pages')) > 0:
            self.index = lambda: flask.redirect('/admin/{}'.format(opt.get('pages')[0]))
        else:
            self.index = AdminHTMLView(self.addHTMLToTemplate('<article class="card c1-1"> <h1>Hej verden</h1> <p>Ingen sidder er oprettet</p> </article>', '')).view
        self.app.add_url_rule('/admin', view_func=self.index)


        # login system
        self.cred = {} #dict
        self.tokens = {} #dict
        self.loginHTML = open(os.path.join(self.absPath, 'login.html'), 'r').read()
        self.loginHTML = self.loginHTML.replace('{mainColor}', opt["color"])
        self.loginHTML = self.loginHTML.replace('{logoSRC}', opt["logo"])
        self.loginHTML = self.loginHTML.replace('{name}', opt["name"])
        self.app.add_url_rule('/admin/login', view_func=self.login, methods = ['POST'])
        self.app.add_url_rule('/admin/logout', view_func=self.logout)


    def addHTMLToTemplate(self, body:str, head:str='', title:str=''):
        return self.template.replace('{body}', body).replace('{head}',head).replace('{nameOfPage}', title)


    def addRule(self, page):
        
        body = ''
        head = ''
        rules = []

        for element in page["body"]:
            
            insertionmark = '{im#'+getid()+'}'
            body += insertionmark
            rules.append([element.body, insertionmark])

            insertionmark = '{im#'+getid()+'}'
            head += insertionmark
            rules.append([element.head, insertionmark])


        view = AdminHTMLView(self.addHTMLToTemplate(body, head, page["name"]), rules)
        rule = '/admin/{}'.format(page["name"].replace(' ', ''))
        self.app.add_url_rule(rule, endpoint=str(getid()), view_func=view.view)


    # login system
    def createSuperUser(self, username:str, psw:str):
        """
        Logger ind med brugernavn og kodeord
        Derefter anvendes en token
        """

        self.cred[username] = psw


    def __getCred__(self):
        if flask.request.cookies.get('userid') and flask.request.cookies.get('atoken'):
            userid = [i for i in flask.request.cookies.getlist("userid") if i != ''][-1]
            token = [i for i in flask.request.cookies.getlist("atoken") if i != ''][-1]
            return userid, token
        else:
            return None, None


    def verify(self):
        
        userid, token = self.__getCred__()

        try:
            tk = self.tokens[userid]
            
            if tk["time"] + self.autoLogoutTime < time.time():
                del self.tokens[userid]
                return False

            if token == tk["token"]:
                return True
        
        except KeyError:
            pass

        if self.debug:
            print('Access not granted, but debug is ON, thereby overwriting protocol')
            return True

        return False


    def login(self):
        
        token = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(24))
        resp = flask.make_response(flask.redirect('/{}'.format(flask.request.form["route"])))
        try:
            if self.cred[flask.request.form["username"]] == flask.request.form["psw"]:
                self.tokens[flask.request.form["username"]] = {"token":token, "time":time.time()}
                resp.set_cookie('atoken', token)
                resp.set_cookie('userid', flask.request.form["username"])

        except KeyError:
            pass

        return resp

    def logout(self):
        try:
            userid, token = self.__getCred__()
            del self.tokens[userid]
        except KeyError:
            pass
        return flask.redirect('/admin')

    def loginRoute(self):
        html = self.loginHTML
        html = html.replace('{clb}', flask.request.url.replace(flask.request.url_root, ''))
        return html


def route():
    flask.request.valter = ''

def update():
    pass


# create a prettier login page
# create custom buttons in table
# create route funciton and update method (attatching something to flask.request)

