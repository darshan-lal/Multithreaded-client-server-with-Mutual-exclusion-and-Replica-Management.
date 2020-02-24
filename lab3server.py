#DARSHAN LAL			
#1001667684			
import threading,time
from threading import Thread,Lock
from Queue import Queue, Empty
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from Tkinter import *
import Tkinter as tk

#ref:https://www.youtube.com/watch?v=0zaPs8OtyKY
lock = Lock()                   #Mutex variable for mutual exclusion
temp=""
temp2=""
f=1
seq_op="1"			#Initial value
pol=0
polstop=0

class RequestHandler(BaseHTTPRequestHandler):
    #the above class is to handle the client request,and below function is to handle Post request
    def do_POST(self):
        global pol

	self.data_string=self.rfile.read(int(self.headers['Content-Length']))
        username, data = self.data_string.split(',')
        msg="Client conected = "+username
        print msg
        self.server.queue.put(msg)
 
	#here is the server thread sleep code
	msg2= "POST request,\nPath: " + str(self.path) + "\nHeaders: " + str(self.headers) + "Body: " + username
        print msg2
        self.server.queue.put(msg2)
        

        self.server.thread_que.put(str(data))	#Putting sequence of operation into the queue
        print "Queue: ",self.server.thread_que

        while 1:
                
                if pol in range(1,polstop+1):
                      msgseq="Sequence of operation from "+username+"="+data
                      self.server.queue.put(msgseq)

                      ans=eval(seq_op+'.0')
                      print ans
                      print str(round(ans, 4))
                      msg3="Server Polls and Pushes : "+str(round(ans, 4))+" to "+username
                      self.server.queue.put(msg3)

                      self.send_response(200)
                      self.end_headers()
                      self.wfile.write(str(round(ans, 4)))
                      print('------POST')
                      lock.acquire()                            #Mutex acquireing the lock
                      pol=pol+1
                      lock.release()                            #Mutex releasing the lock
                      break


        return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass
    #Threadmixin is a library for assiging each client with a single thread to handle the client
    #https://docs.python.org/2/library/socketserver.html
    #https://stackoverflow.com/questions/14088294/multithreaded-web-server-in-python

class Gui(object):
    #A simple GUI 
    def __init__(self, root, queue, thread_que):
        global pol
        
        
        canvas = tk.Canvas(root)
        canvas.pack(side=tk.LEFT,fill="both", expand=True)

        scrollbar = tk.Scrollbar(root, command=canvas.yview)
        scrollbar.pack(side=tk.LEFT, fill='y')

        canvas.configure(yscrollcommand = scrollbar.set)

        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        canvas.bind("<Configure>", self.on_configure(canvas))

        # --- put frame in canvas ---

        frame = tk.Frame(canvas)
        canvas.create_window((0,0), window=frame, anchor='nw')

        # --- add widgets in frame ---
        self.poll_button = tk.Button(frame, text='POLL', command=self.polkol)
        self.poll_button.pack()
        self.queue = queue
        self.thread_que = thread_que
        self.lbl = tk.Label(frame, text="")
        self.lbl.pack()
        self.read_sensor()
        self.read_threadQ()
    
 
    def polkol(self):
        global pol
	global seq_op
	seq_op="1"
        self.read_threadQ()
        pol=1

    def on_configure(self, canvas):
        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        canvas.configure(scrollregion=canvas.bbox('all')) 
        #Data from queue is updated into a label
    
    def read_sensor(self):
        global temp
        global temp2
        global f
        try:
            if f==1:
                  temp=self.queue.get_nowait()
                  f=2
            else:
                  temp2=self.queue.get_nowait()
                  temp=temp+"\n"+temp2
            #display.set(temp)
            self.lbl["text"] = temp
            #self.lbl["text"] = self.queue.get_nowait()
        except Empty:
            pass
        self.lbl.after(527, self.read_sensor)
    
    def read_threadQ(self):
        global seq_op
	global polstop
	print self.thread_que.qsize()
        try:
              while self.thread_que.qsize()!=0:
                polstop=polstop+1
              	seq_op=seq_op+self.thread_que.get_nowait()
              	print seq_op
              	print self.thread_que.qsize()
        except Empty:
              polstop=0
              pass

def main():
    PORT=input('Port?= ')
    #PORT=8976
    #HTTPServer library handles all the socket connection just ip and port is required
    server = ThreadedHTTPServer(('localhost', PORT), RequestHandler)
    server.queue = Queue()
    server.thread_que = Queue()
    msg='Starting server, use <Ctrl-C> to stop'
    print msg
    server.queue.put(msg)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    root = tk.Tk()
    gui = Gui(root, server.queue, server.thread_que)
    root.mainloop()
    server.shutdown()

if __name__ == "__main__":
    main()
