import time
import os, sys

class yklog(object):
    def __init__(self,uid):
        path = sys.path[0]
        if os.path.isfile(path):
            path = os.path.dirname(path)
        self.file = open(path+"/log/"+uid+"-log.txt",'a');
    def logging(self,msg,tj):
        systime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        self.file.write(systime + " " + tj + " : " + msg + "\n")
    def getsuccess(self):
        if self.file is not None:
            return True
        else:
            return False
    def close(self):
        self.file.write("\n\n\n")
        self.file.close()