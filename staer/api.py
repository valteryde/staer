
from .admin import adminList


class ApiHandler:
    def __init__(self):
        pass

    def parse(self, rq):
    
        #verify with admin
        if not adminList[0].verify():
            return False, 'Access not granted'
        
        if rq.args.get('tp') == 'get':
            return ("get", {
                "tablename":  rq.args.get('tbname'),
                "cols" : rq.args.get('p').split('<s>'),
                "query" : rq.args.get('qs')
            })
        
        if rq.args.get('tp') == 'update':
            return ("update", {
                "tablename":  rq.args.get('tbname'),
                "colname" : rq.args.get('key'),
                "value" : rq.args.get('val')
            })
        
        if rq.args.get('tp') == 'delete':
            return ("delete", {
                "tablename":  rq.args.get('tbname'),
                "rowid" : rq.args.get('rid'),
            })
        
        if rq.args.get('tp') == 'create':
            return ("create", {
                "tablename":  rq.args.get('tbname'),
                "columns" : rq.args.get('p').split('<s>'),
                "values" : rq.args.get('val').split('<s>')
            })

        return False, 'Invalid request'