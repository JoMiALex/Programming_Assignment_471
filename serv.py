#python server side TCP
#
#@author John Michael Lott
#@author Mariah Salgado
#@author Tuan Nguyen
#@author Ibrahim Israr

import socket
import sys          
 
s = socket.socket()         
print ("Socket successfully created")
 
port = 12345               

s.bind(('', port))         
print ("socket binded to %s" %(port)) 

s.listen(5)     
print ("socket is listening")            

while True: 
 
  c, addr = s.accept()     
  print ('Got connection from', addr )
 
  
  c.send('Thank you for connecting'.encode()) 
 
  
  c.close()
  
  break