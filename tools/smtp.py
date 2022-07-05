from datetime import datetime
from multiprocessing.dummy import Pool,Lock
import os
import smtplib
import email.message as message
from queue import Queue
from threading import Thread 
try:
    import requests
except:
    os.system("pip install requests")
    import requests
    from requests.auth import HTTPBasicAuth
try:
    import uuid
except:
    os.system("pip install uuid")
    import uuid
class SMTP:
    def __init__(self,bot=False,message_id=False):
        self.bot = bot
        self.message_id = message_id
        self.script_programmer="ZeD_OnE"
        self.gui_programmer="CyberPunk645"
        self.sender_id = "Testing SMTP"
        self.subject = "Consuming"
        self.TEAM= "SuSKod TEAM"
        self.receiver= "spamegytools@gmail.com"
        self.set_data=[]
        self.letter = f"""
        <html>
            <body> <p>Testing SMTP By {message_id}</p></body>
        </html>
        """
    def __set_all_data__(self,x):
        try:
            for receiver in self.receiver:
                data=list(x.split('|'))
                SMTP=data[0]
                email_content=self.letter
                SMTPP__=data[1]
                SMTPU__=data[2]
                _SMTPP__=data[3]
                msg= message.Message()
                try:
                    m= data[4]
                    msg['From']= f"{self.sender_id} <{m}>"
                except:
                    msg['From'] = f"{self.sender_id}<{SMTPU__}>"
                msg['To'] = receiver
                server=SMTP+':'+SMTPP__
                msg['Subject'] = self.subject
                server= smtplib.SMTP(server)
                password = _SMTPP__
                msg.add_header('Content-Type', 'text/html')
                #print(email_content)
                email_content= email_content.replace("SMTP#21",SMTP)
                email_content= email_content.replace("PORT#21",SMTPP__)
                email_content= email_content.replace("USER#21",SMTPU__)
                email_content= email_content.replace("PASS#21",_SMTPP__)
                email_content= email_content.replace("TIMING",str(datetime.now().time()).split(".")[0])
                msg.set_payload(email_content)
                try:
                    server.starttls()
                except:
                    server=SMTP+':'+SMTPP__
                    server= smtplib.SMTP(server)
                server.login(SMTPU__,_SMTPP__)
                server.sendmail(msg['From'],[msg['To']],msg.as_string().encode("UTF-8"))
                print("[Successfully sent] [to {0}][SMTP:{1}]".format(receiver,str(x)))
                with open(f"output/{self.message_id}[SMTP].txt","a+") as p:
                    p.write(str(x)+"\n")
        except Exception as e:
            print(e)
            with open(f"output/{self.message_id}notworking[SMTP].txt","a+") as m:
                m.write("[ERROR:{0}][{1}] \n".format(str(e),str(x)))
    def queue_th_config(self,q):
        while not q.empty():
                i=q.get()
                self.__set_all_data__(i)
                q.task_done()
    def multithreading(self,SMTPS):
        job = Queue()
        for i in SMTPS:
                job.put(i)
        for i in range(10):
                th=Thread(target=self.queue_th_config,args=(job,))
                th.daemon=True
                th.start()
                th.join()
        try:
                newfile = open(f"output/{self.message_id}[SMTP].txt","rb")
                content = newfile.read()
                newfile.close()
                self.bot.send_document(self.message_id,content,caption="Working SMTPS : ",visible_file_name="smtps.txt")
                sec = True
        except:
                sec = False
        try:
                ntfile = open(f"output/{self.message_id}notworking[SMTP].txt","rb")
                content = ntfile.read()
                ntfile.close()
                self.bot.send_document(self.message_id,content,caption="Not Working SMTPS : ",visible_file_name="BadSmtps.txt")
                sec = True
        except:
                pass

        if sec is not True:
            self.bot.send_message(self.message_id,"Error Occured")
