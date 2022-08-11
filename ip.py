
import re
import requests as rq
import json
import os
from datetime import date


# *** document db ***
# ------------------
# fx ip address. (bunk storage)
# ...
# This db will work on a line basis
# that means that lines are NOT
# conntected. Deletion can only be
# done by lines
# An insertion is always append
# ...
# When working with the class
# only on object should be made
# the file worker will be made on
# each request and not at the start
# ------------------
class DocDB:

    def __init__(self, name):
        self.db = os.path.join(name)
        try:
            open(self.db,'x')
            open(self.db,'w').close()
        except FileExistsError:
            pass

        self.get = self._dec_(self._get_)
        self.getAll = self._dec_(self._get_all_)
        self.insert = self._dec_(self._insert_)
        self.find = self._dec_(self._find_)
        self.findAll = self._dec_(self._find_all_)


    def _get_(self, file, line):
        return self._get_all_(file)[line]

    def _get_all_(self, file):
        return [i.split(',') for i in file.read().split('\n')[:-1]]

    def _insert_(self, file, value):
        txt = file.read() #write only appends
        file.write('{}\n'.format(value))

    def _find_(self, file, search, txt=None):
        if not txt: txt = file.read()
        #if not res: return
        try:
            for r in re.finditer('{}'.format(re.escape(search)), txt): #we <3 re
                span = r.span()
                if txt[span[0]-1] not in [',', ' ', '\n']:
                    continue
                if len(txt) != span[1] and txt[span[1]] not in [',', ' ', '\n'] and txt[span[1]:span[1]+1] != '\n':
                    continue
                return txt[:span[0]].count('\n')
        except IndexError:
            pass
        return -1

    def _find_all_(self, file, search, txt=None):
        if not txt: txt = file.read()
        res = []
        try:
            for r in re.finditer('{}'.format(re.escape(search)), txt): #we <3 re
                span = r.span()
                if txt[span[0]-1] not in [',', ' ', '\n']:
                    continue
                if len(txt) != span[1] and txt[span[1]] not in [',', ' ', '\n'] and txt[span[1]:span[1]+1] != '\n':
                    continue
                res.append(txt[:span[0]].count('\n'))
        except IndexError:
            pass
        return res

    # non decorator method
    def overwrite(self, data):
        file = open(self.db, 'w')
        file.write(data)
        file.close()

    # dec
    def _dec_(self, fun):
        def inner(*para):
            file = open(self.db, 'r+')
            res = fun(file, *para)
            file.close()
            return res
        return inner

    def date(self):
        today = date.today()
        return str(today.strftime("%Y/%m/%d"))

# IP collect
class ResNotInPack(Exception): pass
class IPLogger:

    def __init__(self, token=None):
        self.db = DocDB('__ips__.ldb')
        self.token = token

    # method for getting loc
    def getLocationFromIP(self, ip):

        if ip[:7] == '127.0.0':
            return {'country':None, 'error':'Request from localhost'}

        # first search throug RIPE NCC (only in EU)
        # free of charge. (i think)
        tx = rq.get('https://rest.db.ripe.net/search.json?query-string={}'.format(ip))
        packs = json.loads(tx.text)

        try:
            for pack in packs['objects']['object']:
                for att in pack['attributes']['attribute']:

                    if att['name'] == 'country':
                        if att['value'] == 'EU':
                            raise ResNotInPack

                        return {'country':att['value']}
        except ResNotInPack:
            pass

        # second search through ipstack -- https://ipstack.com/
        if not self.token:
            return {"country":None}

        tx = rq.get('http://api.ipstack.com/{}?access_key={}'.format(ip,self.token))
        packs = json.loads(tx.text)
        if packs['country_code']:
            return {'country':packs['country_code'], 'city':packs['city'], 'region':packs['region_name']}
        else:
            return {'country':None, 'error':'No matching ip adress'}


    # method used in routes
    def collect(self, ip):
        search_res = self.db.findAll(ip)
        if not search_res:
            self.db.insert('{},{}'.format(ip, self.db.date()))
            return
        line = self.db.get(search_res[-1]) # get newest
        if line[1] != self.db.date():
            self.db.insert('{},{}'.format(ip, self.db.date()))

    
    def retrieve(self):

        data = {}
        data_list = []
        file = ''
        new_ip_checked = 0
        for i in self.db.getAll():
            if len(i) <= 2:
                ip_res = self.get_loc_ip(i[0])
                new_ip_checked += 1
            elif len(i) >= 4:
                ip_res = {'country':i[2], 'region':i[3], 'city':i[4]}
            else:
                ip_res = {'country':i[2]}
            i = i[:2]
            if ip_res['country']:
                res = i + [ip_res['country']]
                if ip_res.get('region', None): res += ip_res.get('region', ''), ip_res.get('city', '')
                file += '{}\n'.format(','.join(res))
                if ip_res['country'] not in data.keys(): data[ip_res['country']] = []
                data_list.append({**ip_res, 'ip':i[0], 'date':i[1]})
                data[ip_res['country']].append(ip_res)
        self.db.overwrite(file)

        data_count = [(key,len(data[key])) for key in data]
        data_list.reverse()
        return {'data_sorted':data, 'new':new_ip_checked, 'data_count':data_count, 'data_list':data_list}
