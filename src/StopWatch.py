import time

class StopWatch():
    
    def __init__(self):
        self.time = time.time()
    def stop(self):
        time2 = time.time()
        return (time2-self.time)
    
    def stopAndPrint(self):
        print(self.stop())