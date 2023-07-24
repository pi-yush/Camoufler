import logging
import select
import socket
import struct
import os
import base64
import time
from socketserver import ThreadingMixIn, TCPServer, StreamRequestHandler

logging.basicConfig(level=logging.DEBUG)

def exchange_loop(client, remote):
    while True:
        #wait until client or remote is avaiable for read
        r, w, e = select.select([client, remote], [], [])

        if client in r:
            data = client.recv(2048)
            data = base64.b64decode(data)
            #text = text.decode('ascii')
            print("Received Data from client! Forwardng to end server!")
            if remote.send(data) <= 0:
                break

        if remote in r:
            data = remote.recv(2048)
            print("Data recivd from end server")
            if(len(data) > 0):
                encoded = base64.b64encode(data)
                sendable_string = encoded.decode('ascii')
                #print("returned text : " + sendable_string)
                #time.sleep(0.6)
                os.system("python3.6 proxy_data_sender.py " + sendable_string)
            else:
                break
            #back_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #back_client.sendto(data, ("127.0.0.1", 9015))
            #if back_client.send(data) <= 0:
            #    break

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 9014

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

data = client.recv(2048)
print('First data Received from Client')
# Do some processing here to get the address and port
#text = data.decode('ascii')
text = base64.b64decode(data)
text = text.decode('ascii')
print(text)
#address = "1"
#port = "2"

#if text[0] == 'a':
__, address, port = text.split()
port = int(port)
print("Address :" + address + " Port :" + str(port))
    #initial_data = base64.b64decode(b64data)
# Connect to the actual destnation
remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
remote.connect((address, port))
logging.info('Connected to %s %s' % (address,port))
#remote.send(initial_data)

exchange_loop(client, remote)
