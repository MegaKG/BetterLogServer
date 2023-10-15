#GNU General Public License v3.0
#Code by MegaKG
import mimetypes

#This file contains the base class for all webpages to be based off

class webpage:
    #This shouldn't ever be overwritten by the child
    def __init__(self,Options):
        self.Options = Options
        self._Connection = None

    def acceptConnection(self,CON):
        self._Connection = CON

    #Me First
    def sendCode(self, Code):
        self._Connection.sendstdat("HTTP/1.1 " + str(Code) + " \nServer: KPython V4\nVary: Accept-Encoding\n")

    #Me Last
    def sendType(self,Mime):
        self._Connection.sendstdat("Content-Type: " + Mime + "\n\n")

    #Required for continual connections
    def sendLength(self,Length):
        self._Connection.sendstdat("Content-Length: " + str(Length) + "\n")

    #Custom Headers
    def sendHeader(self,Key,Value):
        self._Connection.sendstdat("{}: {}\n".format(Key,Value))

    #Makes life easy for page generation
    def print(self,*IN):
        OUTST = ''
        for i in IN:
            OUTST += str(i) + ' '
        OUTST = OUTST[:-1].encode('utf-8')
        self._Connection.senddat(OUTST)

    def mimeFromFileExtension(self,Path):
        return mimetypes.guess_type(Path)

    def close(self):
        self._Connection.close()

    #Deconstructor
    #def __del__(self):
        #self.Connection.close()
    
    def getConnectionObject(self):
        return self._Connection

    

    #These are User replacable functions in the child classes
    def connect(self):
        pass

    def webSocket(self):
        self.close()

    