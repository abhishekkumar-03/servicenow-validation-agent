
import requests
from requests.auth import HTTPBasicAuth
class ServiceNowService:
    def __init__(self,url,user,password):
        self.url=url; self.user=user; self.password=password
    def get_validations(self):
        r=requests.get(f"{self.url}/api/now/table/task",auth=HTTPBasicAuth(self.user,self.password),params={"sysparm_limit":"100"})
        return r.json().get("result",[])
