#darshan lal
#1001667684


import http.client						# it handles all the connection no need to worry about socket
#ref: https://docs.python.org/3/library/http.client.html

import sys,os.path							#For checking if a persistence storage file is present or not 

#GUI Library
if sys.version_info[0] == 2:
    from Tkinter import *					#importing the GUI library
else:
    from tkinter import *


PORT=int(input("Port?="))					#Port input
#PORT= 8976


conn = http.client.HTTPConnection('localhost',PORT)		# it handles all the connection no need to worry about socket
#ref:https://www.journaldev.com/19213/python-http-client-request-get-post

#This class handle the Gui
class MyFirstGUI(Frame):
    def __init__(self, master=None):
        self.master = master
        master.title("Client 2 GUI")

        self.label = Label(master, text="To Start a client press start ")
        self.label.pack()

        self.entry=Entry(master)						#User input from GUI
        self.entry.pack()
        
        self.start_button = Button(master, text="Start", command=self.Send)	#Start button
        self.start_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)	#Close button
        self.close_button.pack()

        self.label3 = Label(master, text="")					#Label to display user input
        self.label3.pack()

        self.label2 = Label(master, text="")					#To display the server response
        self.label2.pack()

        
    
    #This function dynamically updates the label when response is received from the server 
    def updatetext(self,response,readableresponse):
        self.response=response
        self.readableresponse=readableresponse
        msg= str(response.headers)+str(response.status)+str(response.reason)+"\nResponse received from server : "
        msg2=str(response)+"\nResponse after decoding : "+readableresponse
        msg3="\nInitial value is updated to : "+readableresponse+"\nThankyou"
        self.label2["text"] = msg+msg2+msg3
        return

    #This function display what you have entered
    def youentered(self,cal,evaluate,i):
        self.cal=cal
        disptxt= "Initial value = "+i+"\n"+i+str(cal) +"="+ str(evaluate)
        self.label3["text"] = disptxt
        return

    #This function takes care of message sending and receiving to/from the server
    def Send(self):
               
        #https://stackoverflow.com/questions/3346430/what-is-the-most-efficient-way-to-get-first-and-last-line-of-a-text-file
        #Below lines will check for the file and will take out the latest server push value and use it as the initial value
        if os.path.isfile("client2.txt"):
               f=open("client2.txt", "r")
               fl =f.readlines()
               for line in fl: pass
               print("last line :",line)
               if "-"==line[:1]:
                     i=line[:2]
                     #i=i+line[:2]
               else:
                    i=line[:1]
        else:
            print("file doesnot exist")
            i="1"

        print("initial :",i)
        
	#Calculation of the user input at client side on client's initial value
        cal=str(self.entry.get())
        ical=i+cal
        evaluate=str(round(eval(ical), 4))
        print(cal)
        print(evaluate)
        self.youentered(cal,evaluate,i)
        
        headers = {'Content-type': 'text'}
        data="Client 2,"
        
        final=data+cal								#Soncatinating seq of operation with username
        
        print("Username : ",data)
        
        conn.request('POST', '/post', final, headers) 				#Sending the POST request to server	
        
        response = conn.getresponse()		      				#Here response is received
        

        print(response.headers)
        print(response.status, response.reason) # 200 ok
        print("Response received from server : ",response)
        readableresponse=response.read().decode('ascii')
        print("Response after decoding :",readableresponse)

        
        #Logging the response in persistance storage
        if os.path.isfile("client2.txt"):
             f= open("client2.txt","a+")
        else:
             f= open("client2.txt","w+")
        
        f.write(cal+"\n")							#Writting the seq of operation onto the text file 
        f.write(readableresponse+"\n")						#Writting the server push value to the text file
        f.close()
        
        self.updatetext(response,readableresponse)				#Function call to display server response
        return

root = Tk()
root.geometry("1000x250")

my_gui = MyFirstGUI(root)
root.mainloop() 
