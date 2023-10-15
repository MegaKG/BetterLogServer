class statistics:
    def __init__(self,HostIP='0.0.0.0',HostPort=5000):
        self.watchArray = {}

    def addStatistic(self,watchArray):
        self.watchArray = watchArray

    def run(self):
        pass