from socket import *
from Safe_Part import *
def send_string(client, message):
  client.send(bytes(message, encoding='utf-8'))
  
def recv_string(client):
  return client.recv(1024).decode('utf-8')

Client = socket(AF_INET,SOCK_STREAM)
Client.connect('127.0.0.1',8888)

def Register(client) :
    print(recv_string(client))
    string=recv_string(client)
    while(string!="Input your password::"):
        print(string)
        string=recv_string(client)
    
myPublickey,myPrivatekey=generate_key_pair()
print(recv_string(Client))
string=input()
while input != "Register" and input != "Login":
  print("Wrong Input! Please input Register or Login!")
  string=input()
if string == "Register" :
    Register(Client)
Login(Client)
    