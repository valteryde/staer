
import os
import flask
from .admin import routes, adminList
from .id import getid
import shutil


# file explorer
uploadRouteMade = False
class FileExplorer:
    def head(self): 
        return '<script>const file{} = new FilePreview({});</script>'.format(self.id, self.id)
    
    def __init__(self, folder:str, handler:any=None, deletable:bool=False, size:tuple=(2,2)):
        global uploadRouteMade
        
        absPath = os.path.dirname(__file__)
        self.html = open(os.path.join(absPath, 'component', 'file.html'), 'r').read()
        self.folder = folder
        self.handler = handler

        self.id = getid()

        self.html = self.html.replace('{width}', str(size[0]))
        self.html = self.html.replace('{height}', str(size[1]))
        self.html = self.html.replace('{folderName}', folder)
        self.html = self.html.replace('{id}', self.id)
        
        self.deletable = deletable
        if not self.deletable:
            self.html = self.html.replace('{show}', 'display:none')
        
        if deletable:
            
            if 'bin' not in os.listdir():
                os.mkdir('bin')
            
            if self.folder not in os.listdir('bin'):
                os.path.join('bin', self.folder)

        routes.append(('/{}{}/<string:filename>'.format(folder, self.id), self.fileSendRoute))
        routes.append(('/{}{}/'.format(folder, self.id), self.__fileSendRouteRoot__))

        if not uploadRouteMade:
            routes.append(('/admin/uploadFile'.format(folder), self.uploadFileRoute, ['POST']))
            uploadRouteMade = True


    def __fileSendRouteRoot__(self):
        adminList[0].verify()
        return self.fileSendRoute('')


    def __moveFile__(self, src:str, dst:str):

        # add folder(s)
        folders = dst.split(os.path.sep)[:-1]
        for i, folder in enumerate(folders):
            if i == 0:
                continue

            pfolder = os.path.join(*folders[:i])
            if folder not in os.listdir(pfolder):
                os.mkdir(os.path.join(pfolder, folder))

        # move file
        shutil.move(src, dst)


    def fileSendRoute(self, filename:str):
        adminList[0].verify()
        
        if flask.request.args.get('delete') and self.deletable:
            path = os.path.join(self.folder, filename.replace('-', os.path.sep))
            self.__moveFile__(path, os.path.join('bin', path))
            
            return '', 200

        if flask.request.args.get('download'): #download
            return flask.send_file(os.path.join(self.folder,filename.replace('-', os.path.sep)), as_attachment=True)
        else: #preview
            if '.' in filename:
                return flask.send_file(os.path.join(self.folder,filename.replace('-', os.path.sep)))
            else:
                return self.__rule__(filename)


    def uploadFileRoute(self):
        adminList[0].verify()

        file = flask.request.files['file']
        
        path = flask.request.form.get('path')
        if path:
            path = os.path.join(self.folder, path.replace('-', os.path.sep), file.filename)[1:]
            temp = os.path.join(self.folder, file.filename)
            file.save(temp)
            self.__moveFile__(temp, path)
        else:
            file.save(os.path.join(self.folder, file.filename))

        return flask.redirect(flask.request.referrer)


    def body(self): 
        return self.html.replace('{files}', self.__rule__())


    def __rule__(self, folder:str=None):

        if not folder:
            files = os.listdir(self.folder)
        else:
            folder = folder.replace('-', os.path.sep)
            files = os.listdir(os.path.join(self.folder,folder))

        innerhtml = ''

        for i in files:
            
            tp = i.split('.')[-1]            
            
            if tp == i:
                icon = '<span class="material-symbols-outlined">folder</span>'

            elif tp in ['png', 'jpg', 'jpeg', 'gif', 'PNG', 'JPG', 'tiff', 'HEIC']:
                icon = '<span class="material-symbols-outlined">image</span>'

            else:
                icon = '<span class="material-symbols-outlined">draft</span>'

            if folder:
                url = '/{}{}/{}-{}'.format(self.folder, self.id, folder.replace(os.path.sep,'-'), i)
            else:
                url = '/{}{}/{}'.format(self.folder, self.id, i)
            innerhtml += '<div onclick="file{}.click(`{}`, this)" class="file">{}<p>{}</p></div>'.format(self.id, url, icon, i)

        return innerhtml

