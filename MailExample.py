Python 3.8.10 (default, Jun 22 2022, 20:18:18) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license()" for more information.
>>> 
========== RESTART: /media/kaelan/Disk/Dev/FinalLogServer/Sendmail2.py =========
>>> a = MIMEMultipart("alternative")
>>> a["Subject"] = "HELLO"
>>> a["From"] = "kaelan@isnet.local"
>>> a["To"] = "graings@isnet.local"
>>> a.attach(MIMEText("world","html"))
>>> a.to_string()
Traceback (most recent call last):
  File "/usr/lib/python3.8/idlelib/run.py", line 559, in runcode
    exec(code, self.locals)
  File "<pyshell#5>", line 1, in <module>
AttributeError: 'MIMEMultipart' object has no attribute 'to_string'
>>> a.as_string()
'Content-Type: multipart/alternative; boundary="===============0872637356250948770=="\nMIME-Version: 1.0\nSubject: HELLO\nFrom: kaelan@isnet.local\nTo: graings@isnet.local\n\n--===============0872637356250948770==\nContent-Type: text/html; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\n\nworld\n--===============0872637356250948770==--\n'
>>> 