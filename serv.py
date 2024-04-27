#python server side TCP
#
#@author John Michael Lott
#@author Mariah Salgado
#@author Tuan Nguyen
#@author Ibrahim Israr

import socket
import sys

def dataReciever(sock, rSize):
  #data buffers
	rBuff = ""
	
	tBuff = ""
	
  #Recieve data of specified size
	while len(rBuff) < rSize:
		
		tBuff =  sock.recv(rSize)
		
		if not tBuff:
			break
		
		rBuff += tBuff
	
	return rBuff
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
print ("Socket successfully created")
 
port = 12345               

s.bind(('', port))         
print ("socket binded to %s" %(port)) 

s.listen(5)     
print ("socket is listening")            

while True: 
 
  c, addr = s.accept()     
  print ('Got connection from', addr )
  while True:
    rBuff = ""
    fileData = ""
    fileSize = 0
    fSizeBuff = ""

    fSizeBuff = dataReciever(c, 10)

    fileSize = int(fSizeBuff)
    print("The file size is ", fileSize)

    fileData = dataReciever(c, fileSize)

    print("The file data is: ", fileData)
    continue
  
  c.send('Thank you for connecting'.encode()) 
 
  
  c.close()
  
  break