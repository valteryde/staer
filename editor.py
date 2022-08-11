
import glob
import json
import os
import flask
from .id import getid, getFilename
from .admin import routes, adminList
from base64 import b64decode


class Editor:
    def __init__(self, folder, title, showFiles:bool=True, size:tuple=(3,1)):
        absPath = os.path.dirname(__file__)
        self.html = open(os.path.join(absPath, 'component', 'editor.html'), 'r').read()
        self.id = getid()
        self.html = self.html.replace('{width}', str(size[0]))
        self.html = self.html.replace('{height}', str(size[1]))
        self.html = self.html.replace('{title}', title)

        self.html = self.html.replace('{id}', self.id)

        self.mediapath = os.path.join(folder,'media')
        if not os.path.isdir(self.mediapath):
            os.mkdir(self.mediapath)

        self.folderpath = os.path.join(folder,'doc')
        if not os.path.isdir(self.folderpath):
            os.mkdir(self.folderpath)
        
        routes.append(('/admin/editor/save/{}'.format(self.id), self.saveRoute, ["POST"]))
        routes.append(('/admin/editor/delete/{}'.format(self.id), self.deleteRoute))
        routes.append(('/admin/editor/open/{}'.format(self.id), self.openRoute))
        routes.append(('/admin/editor/rename/{}'.format(self.id), self.renmaeRoute))
        routes.append(('/admin/editor/media/{}/<string:filename>'.format(self.id), self.uploadMedia))


    # routes
    def saveRoute(self):
        adminList[0].verify()

        data = flask.request.get_json()
        body = data["body"]["ops"]
        
        if data["filename"] == "":
            data["filename"] = getFilename(self.folderpath)

        for i, line in enumerate(body):
            if type(line["insert"]) is dict:
                image64Spacer = 'data:image'
                
                if line["insert"]["image"][:len(image64Spacer)] != image64Spacer:
                    continue

                filename = '{}.png'.format(getFilename(self.mediapath))
                filepath = os.path.join(self.mediapath, filename)
                image = open(filepath, 'wb')
                image.write(b64decode(line["insert"]["image"][line["insert"]["image"].index(','):]))
                image.close()

                line["insert"] = {"image": filename}


        file = open('{}.json'.format(os.path.join(self.folderpath, data["filename"])), 'w')
        file.write(json.dumps(data["body"], indent=4))
        file.close()

        return flask.jsonify({
            "html": self.getFilesPreview(),
            "filename": data["filename"]
        })


    def openRoute(self):
        adminList[0].verify()

        filename = flask.request.args.get('filename')
        j = json.load(open(os.path.join(self.folderpath, '{}.json'.format(filename)), 'r'))

        for i in j["ops"]:
            if type(i["insert"]) is dict:
                i["insert"] = {"image": '/admin/editor/media/{}/{}'.format(self.id,i["insert"]["image"])}

        return flask.jsonify(j)


    def deleteRoute(self):
        adminList[0].verify()

        filename = flask.request.args.get('filename')
        if filename == "":
            return '', 200
        
        j = json.load(open(os.path.join(self.folderpath, '{}.json'.format(filename)), 'r'))

        medias = []
        for i in j["ops"]:
            if type(i["insert"]) is dict:
                medias.append(i["insert"]["image"])
        
        os.remove(os.path.join(self.folderpath, '{}.json'.format(filename)))
        for i in medias:
            os.remove(os.path.join(self.mediapath, i))

        return '', 200


    def renmaeRoute(self):
        adminList[0].verify()
        
        # check for overwrite in filenames
        filename = flask.request.args.get('new')
        os.rename(
            os.path.join(self.folderpath, '{}.json'.format(flask.request.args.get('old'))), 
            os.path.join(self.folderpath, '{}.json'.format(filename))
        )
        return filename

    
    def uploadMedia(self, filename:str):
        adminList[0].verify()
        return flask.send_file(os.path.join(self.mediapath, filename))

    
    # other
    def getFilesPreview(self):
        
        filesHTML = ''
        for file in glob.glob(os.path.join(self.folderpath, '*.json')):
            file = os.path.split(file)[-1]

            filesHTML += """
            <div onclick="editor{id}.open(`{title}`)" class="filebar-file">
                <div>
                    <span class="icon material-symbols-outlined">article</span>
                    {title}
                </div>
            </div>
            """.replace('{title}', file.split('.')[0]).replace('{id}', self.id)

        return filesHTML

    # element
    def head(self):
        return """
            <script src="//cdn.quilljs.com/1.3.6/quill.min.js"></script>
            <link href="//cdn.quilljs.com/1.3.6/quill.snow.css" rel="stylesheet">
        """

    def body(self):
        return self.html.replace('{files}', str(self.getFilesPreview()))
