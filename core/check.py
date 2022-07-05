import pyrebase
import time


class CheckDb:
    def __init__(self) -> None:
        self.firebaseConfig = {
            "apiKey": "AIzaSyAf4s5E1cJU7sovPNlnCw_-gkVfUFdZwxQ",
            "authDomain": "spamegy-8a7d3.firebaseapp.com",
            "projectId": "spamegy-8a7d3",
            "storageBucket": "spamegy-8a7d3.appspot.com",
            "messagingSenderId": "388468064607",
            "appId": "1:388468064607:web:0b14d2cd2ef95cfd7336ea",
            "measurementId": "G-1VM7F2LLTD",
            "databaseURL": "https://spamegy-8a7d3-default-rtdb.firebaseio.com"
            }
        firebase = pyrebase.initialize_app(self.firebaseConfig)
        self.db = firebase.database()
    def getFreeTrial(self,id):
        try:
            retreived = self.db.child(id).get()
            mac = retreived.val()['trial']
            return False
        except:
            self.db.child(id).update({"trial":f"{time.time()+900}"})
            return True
    def verify(self,id):
        try:
            '''
            Retreiving key and data
            '''
            retreived = self.db.child(id).get()
            mac = retreived.val()['exist']
            return True
        except:
            try:
                retreived = self.db.child(id).get()
                mac = retreived.val()['trial']
                print(mac)
                if time.time()<float(mac):
                    return True
                else:
                    raise Exception
            except Exception as e:
                print(e)
                return False
    def setVar(self,id,var):
        self.db.child(id).update({"set":var})
    def getVar(self,id):
        try:
            var = self.db.child(id).get().val()["set"]
            return var
        except:
            return False
    def delVar(self,id):
        self.db.child(id).update({"set":"none"})