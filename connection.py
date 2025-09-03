import config
import requests
import json

class Connection():
    def __init__(self):
        self.base_url = config.base_url
    
    def post(self, url, payload):
        end_point = self.base_url + url
        try:
            r = requests.post(end_point, data=json.dumps(payload))
            if r.status_code == requests.codes.ok:
                return r.json()
            else:
                print('Bad Request', r.status_code)
        except:
            print("Bad request", r.status_code)
        return False
    
    def get(self, url, payload = {}):
        end_point = self.base_url + url
        try:
            r = requests.get(end_point, params=payload)
            if r.status_code == requests.codes.ok:
                return r.json()
            else:
                print('Bad Request', r.status_code)
        except:
            print("Bad request, server down ?")
        return False