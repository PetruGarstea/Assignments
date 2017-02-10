import sys
import socket

def syslog_server():
    
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(('127.0.0.1', 5005))
    listener.listen(5)
    
    while True:
        
        conn, addr = listener.accept()
#       print 'Connection address:', addr
        
        data = conn.recv(1024)
        print data
        
        conn.send('ACK')
        
        conn.close()

syslog_server()