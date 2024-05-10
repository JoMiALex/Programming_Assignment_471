# Programming Assignment CPSC 471

Names and email addresses of all partners:
  John Michael Lott - jlott1004@csu.fullerton.edu
  Mariah Salgado - mariahhsall@csu.fullerton.edu
  Tuan Nguyen - tnguyen527@csu.fullerton.edu
  Ibrahim Israr - misrar0@csu.fullerton.edu

The programming language: python

How to execute the program:  
  The ftp client is invoked as: python client.py <server port>
    For example: python cli.py 127.0.0.1 54123
    <server machine> is the domain name of the server (ecs.fullerton.edu). 
    <server port> is the port number of server (54123)
    This will be converted into 32 bit IP address using DNS lookup. 
    Upon connecting to the server, the client prints out ftp>, which allows the user to execute
    the following commands:  
      ftp> get <file name> (downloads file <file name> from the server)
      ftp> put <filename> (uploads file <file name> to the server)
      ftp> ls(lists files on theserver)
      ftp> quit (disconnects from the server and exits)
    
  The server shall be invoked as: python serv.py <PORTNUMBER>
    <PORT NUMBER>specifies the port at which ftp server accepts connection requests.
    For example: python serv.py 1234 

