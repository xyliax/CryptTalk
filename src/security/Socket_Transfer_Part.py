import time
def send_string(client, message):
  client.send(bytes(message, encoding='utf-8'))
  time.sleep(2)
  
def recv_string(client):
  string=client.recv(2100).decode('utf-8')
  time.sleep(2)
  return string

def send_byte(client,message) :
  client.send(message)
  time.sleep(2)

def recv_byte(client) :
  byte= client.recv(2100)
  time.sleep(2)
  return byte
