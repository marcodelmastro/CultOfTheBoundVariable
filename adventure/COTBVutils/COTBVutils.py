from subprocess import Popen, PIPE
from threading  import Thread
from queue import Queue, Empty
import time

class InteractiveProcess:

    def enqueue_output(self,out,queue):
        '''Enqueue output from process STDOUT in queue'''
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()
    
    def read_output(self):
        '''Read output enqueued in queue until empty, then return it'''
        output = ""
        while True:
            try:
                output += (self.q.get(block=False)).decode()
            except Empty:
                return output
            
    def send_command(self,c,sleeptime=0.2):
        '''Send a command to process STDIN'''
        self.p.stdin.write((c+"\n").encode())
        self.p.stdin.flush()
        if sleeptime:
            time.sleep(sleeptime)
        return self.read_output()
    
    def __init__(self,process,sleeptime=0):
        self.p = Popen(process.split(),stdin=PIPE,stdout=PIPE,stderr=PIPE,close_fds=True)
        self.q = Queue()
        self.t = Thread(target=self.enqueue_output, args=(self.p.stdout,self.q))
        self.t.daemon = True # thread dies with the program
        self.t.start()
        if sleeptime:
            time.sleep(sleeptime)
        #print(self.read_output())
