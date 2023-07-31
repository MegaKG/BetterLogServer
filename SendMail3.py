import smtplib
import ssl

class emailer:
    def __init__(self,server,email,username,password,port=587):
        self.port = 587
        self.username = username
        self.password = password
        self.serveraddr = server
        self.server = False
        self.emailaddr = email

    def connect(self):
        self.server = smtplib.SMTP(self.serveraddr,self.port)

    def starttls(self):
        context = ssl.create_default_context()

        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        self.server.ehlo()
        self.server.starttls(context=context)
        self.server.ehlo()

    def login(self):
        self.server.login(self.username, self.password)

    def email(self,addr,msg):
        self.server.sendmail(self.emailaddr, addr, msg)

    def disconnect(self):
        self.server.close()

    
    


