import logging
import select
import socket
import struct
import os
import base64
import time
from socketserver import ThreadingMixIn, TCPServer, StreamRequestHandler

logging.basicConfig(level=logging.DEBUG)

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 9013

class ThreadingTCPServer(ThreadingMixIn, TCPServer):
    pass


class SocksProxy(StreamRequestHandler):

    def handle(self):
        logging.info('Accepting connection from %s:%s' % self.client_address)

        try:
            #if cmd == 1:  # CONNECT
                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote.connect((UDP_IP_ADDRESS, UDP_PORT_NO))
                #remote = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                #remote.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
            #else:
                #self.server.close_request(self.request)


        except Exception as err:
            logging.error(err)

        # establish data exchange
        self.exchange_loop(self.connection, remote)

        self.server.close_request(self.request)

    def exchange_loop(self, client, remote):

        while True:

            # wait until client or remote is available for read
            r, w, e = select.select([client, remote], [], [])

            if client in r:
                data = client.recv(2048)
                if(len(data) <=0):
                    break;
                #print(client)
                #Encode the data to base64 for easily sending it as an argument
                encoded = base64.b64encode(data)
                sendable_string = encoded.decode('ascii')
                print("Data sent to IM App!")
                #time.sleep(0.5)
                os.system('python3.6 client_requester.py ' + sendable_string)

            if remote in r:
                data = remote.recv(2048)
                if(len(data) <= 0):
                   break;
               
                final = base64.b64decode(data) 
                print("Data received from IM App!")
                #print("Received data " + str(data) + "\n Decoded data " + str(final))
                if client.send(final) <= 0:
                    break


if __name__ == '__main__':
    server = ThreadingTCPServer(('127.0.0.1', 9012), SocksProxy)
    server.serve_forever()

