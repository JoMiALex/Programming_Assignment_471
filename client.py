#python client side TCP
#
#@author John Michael Lott
#@author Mariah Salgado
#@author Tuan Nguyen
#@author Ibrahim Israr

import socket             

s = socket.socket()         

port = 12345               

s.connect(('127.0.0.1', port)) 

print (s.recv(1024).decode())

s.close()