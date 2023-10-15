#!/usr/bin/env python3
import time
import threading
import Engines.SendMail3 as SendMail3
from Engines.HTML_PY import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import mysql.connector as mc

class emailer:
    def __init__(self,server,email,user,password,port,subject):
        self.urgent = []
        self.subject = subject
        self.eml = SendMail3.emailer(
            server,
            email,
            user,
            password,
            port
        )

    def appendUrgent(self,record):
        self.urgent.append(record)

    def _logDecode(self,IN):
        Out = ''
        for i in IN:
            Out += chr(i)
        return Out

    def _generateUrgent(self):
        TABLE = table(tr(th("Message")))
        for log in self.urgent:
            TABLE.append(
                tr(
                    td(self._logDecode(log))
                )
            )

        Message = html(
            header(
                h("System Alert",2)
            ),
            body(
                h("The following logs were captured:",3),
                italic(datetime.datetime.now()),
                br(),
                TABLE
            )
        )

        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.subject
        msg['From'] = self.config['emailuser']
        conv = MIMEText(str(Message), 'html')

        msg.attach(conv)

        return msg.as_string()


        

    def _mainthread(self):
        while True:
            time.sleep(60)

            if len(self.urgent) > 0:
                msg = self._generateUrgent()
                self.urgent = []
                self.eml.connect()
                self.eml.starttls()
                self.eml.login()

                for addr in self.config['emailtargets']:
                    self.eml.email(addr,msg)
                self.eml.disconnect()




    def start(self):
        self.myThread = threading.Thread(target=self._mainthread,name='Emailer')
        self.myThread.start()
