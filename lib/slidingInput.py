class slidingInput:
    def __init__(self,denoteby,maxbuf):
        self.denoteby = denoteby
        self.buffer = []
        self.maxbuf = maxbuf
    
    def add(self,data):
        for i in data:
            self.buffer.append(i)

    def getavailable(self):
        Out = []

        temp = bytearray()
        wordl = 0
        lastend = 0
        for count in range(len(self.buffer)):
            if (self.buffer[count] == self.denoteby) or (wordl == self.maxbuf):
                Out.append(bytes(temp))
                temp.clear()
                wordl = 0
                lastend = count
            else:
                wordl += 1
                temp.append(self.buffer[count])

        self.buffer = self.buffer[lastend:]
        return Out