from socket import *

def send_string(client, message):
  client.send(bytes(message, encoding='utf-8'))
  
def recv_string(client):
  return client.recv(1024).decode('utf-8')

Client = socket(AF_INET,SOCK_STREAM)
Client.connect('127.0.0.1',8888)
