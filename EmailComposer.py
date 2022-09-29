#!/usr/bin/env python3
import time
import threading
import SendMail3
from HTML_PY import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import mysql.connector as mc

class emailer:
    def __init__(self,config):
        self.urgent = []
        self.config = config
        self.eml = SendMail3.emailer(
            config['smtpserver'],
            config['email'],
            config['emailuser'],
            config['emailpass'],
            config['emailport']
        )

    def appendUrgent(self,record):
        self.urgent.append(record)

    def _logDecode(self,IN):
        Out = ''
        for i in IN:
            Out += chr(i)
        return Out

    def _generateWeekly(self):
        self.Con = mc.connect(
                host = self.config['dbhost'],
                user = self.config['dbuser'],
                passwd = self.config['dbpass'],
                database = self.config['dbdata'],
                port = self.config['dbport']
            )
        self.Cursor = self.Con.cursor()

    def _generateDaily(self):
        pass



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
        msg['Subject'] = "Log Alert"
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
