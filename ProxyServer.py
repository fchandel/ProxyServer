from socket import *
import sys

if len(sys.argv) <= 1:
	print(
	    'Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
	sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# bind the socket to a host, and a port
tcpSerSock.bind(("localhost", 8888))
# listen for messages
tcpSerSock.listen(1)


while 1:
	# Start receiving data from the client
	print('Ready to serve...')
	tcpCliSock, addr = tcpSerSock.accept()
	print('Received a connection from:', addr)
	message = tcpCliSock.recv(4096).decode()
	print('start: ')
	print(message)
	# Extract the filename from the given message
	print(message.split()[1])
	filename = message.split()[1].partition("/")[2]
	print(filename)
	fileExist = "false"
	filetouse = "/" + filename
	print(filetouse)
	try:
		# Check wether the file exist in the cache
		f = open(filetouse[1:], "r")
		outputdata = f.readlines()
		fileExist = "true"
		# ProxyServer finds a cache hit and generates a response message
		tcpCliSock.send("HTTP/1.0 200 OK\r\n")
		tcpCliSock.send("Content-Type:text/html\r\n")
			
		print('Reading from cache')
		for line in outputdata:
			tcpCliSock.send(line)
		
		print('Read from cache')
	# Error handling for file not found in cache
	except IOError:
		if fileExist == "false":
			# Create a socket on the proxyserver
			c = socket(AF_INET, SOCK_STREAM)
			hostn = filename.replace("www.","",1)         
			print("host: ", hostn)      
			if (hostn == 'favicon.ico'):
				print("404 Error. File not found")
				tcpCliSock.send("HTTP/1.0 404 Not Found\r\n")
			else:
				try:
					# Connect to the socket to port 80
					c.connect((hostn, 80))

					print("connected to host port 80")                                                        
					# Create a temporary file on this socket and ask port 80 for the file requested by the client
					fileobj = c.makefile('r', 0)    
					fileobj.write("GET "+"http://" + filename + " HTTP/1.0\n\n")  
					print("written open")                                                        
		
					# Read the response into buffer
					buffer = fileobj.readlines()
					print("buffer read")                                            
		
			
					# Create a new file in the cache for the requested file. Also send the response in the buffer to client socket and the corresponding file in the cache
					tmpFile = open("./" + filename,"wb")  
					print("file open")                                                        
					
					for line in buffer:
						tmpFile.write(line)
						tcpCliSock.send(line)
					
					print("file written")                                                        
		
				except AssertionError as error:
					print(error)
					print("Illegal request")
					break
		else:
			# HTTP response message for file not found
			print("404 Error. File not found")
			tcpCliSock.send("HTTP/1.0 404 Not Found\r\n")
   
   
	# Close the client and the server sockets    
	tcpCliSock.close() 
tcpSerSock.close()