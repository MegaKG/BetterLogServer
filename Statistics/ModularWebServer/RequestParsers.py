#GNU General Public License v3.0
#Code by MegaKG
class RequestParser:
    def __init__(self):
        pass

    #This processes GET requests
    def procGet(self,GETR):
        RET = {}
        for pair in GETR.split('&'):
                    SP = pair.split('=')
                    RET[SP[0]] = SP[1].replace('+',' ')
        return RET

    #Merges two dictionaries, internal method
    def _dictMerge(self,D1,D2):
        for key in D1:
            D2[key] = D1[key]
        return D2

    #This parses HTTP request headers from the client
    def parseRequest(self,Req):
        #First Get the Request type and resource
        #(Req)
        SP = Req.strip(b'\r').split(b'\n')
        Resource = SP[0].decode()

        #Process HTTP Attributes in the request
        OUT = {}
        OUT["GET"] = {}
        OUT["POST"] = {}

        #Process GET values
        Resource = Resource.split(' ')[1]
        if '?' in Resource:
            Resource,GET = Resource.split('?')
            OUT["GET"] = self.procGet(GET)


        #Process POST values 
        for i in SP[1:]:
            if (len(i) > 3) and (b':' in i):
                REQ_SP = i.split(b': ')
                OUT[REQ_SP[0].decode()] = REQ_SP[1].strip(b'\r')
            elif b'=' in i:
                OUT["POST"] = self._dictMerge(OUT["POST"],self.procGet(i))

        return OUT,Resource