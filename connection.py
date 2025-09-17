import config
import requests
import json

class Connection():
    def __init__(self):
        self.base_url = config.base_url
        self.s = requests.Session()
    
    def post(self, url, payload):
        end_point = self.base_url + url
        try:
            r = self.s.post(end_point, data=json.dumps(payload))
            if r.status_code == requests.codes.ok:
                return (True, r.json())
            else:
                print('Bad Request', r.status_code)
                return (False, r.status_code)
        except Exception as err:
            print("Bad request", err)
        return False
    
    def put(self, url, payload = {}):
        end_point = self.base_url + url
        try:
            r = self.s.put(end_point, data=json.dumps(payload))
            if r.status_code == requests.codes.ok:
                return (True, r.json())
            else:
                print('Bad Request', r.status_code)
                return (False, r.status_code)
        except Exception as err:
            print("Bad request", err)
        return False

    def get(self, url, payload = {}):
        end_point = self.base_url + url
        try:
            r = self.s.get(end_point, params=payload)
            if r.status_code == requests.codes.ok:
                return (True, r.json())
            else:
                print('Bad Request', r.status_code)
                return (False, r.status_code)
        except Exception as err:
            print("Bad request", err)
        return False