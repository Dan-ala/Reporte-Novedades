import json,requests
class Usuario:
    url=None
    res=None
    data=None
    def __init__(self,murl='http://192.168.77.59:5000'):
        self.url=murl

    def ListarTodos(self):
        self.res=requests.get(self.url+"/to")
        data1=json.loads(self.res.content)
        return data1

    def ListarUno(self, cual=0):
        try:
            self.res = requests.get(self.url + "/" + str(cual))
            if self.res.status_code == 200:
                data1 = json.loads(self.res.content)
                if data1 != []:
                    return data1
                else:
                    return None
            else:
                print("Error: ", self.res.status_code)
                return None
        except Exception as e:
            print("An error occurred:", e)
            return None

    def Inserte(self,data):
        response = requests.post(self.url+"/i", json=data)
    def Borra(self,cual):
        response = requests.delete(self.url+"/d/"+str(cual))
    def BorraTodo(self):
        response = requests.delete(self.url+"/d")
    def Actualiza(self,data):
        response = requests.put(self.url+"/u", json=data)