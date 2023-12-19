from socket import *
from Safe_Part import *
from Database_Part import *
import time
def send_string(client, message):
  client.send(bytes(message, encoding='utf-8'))
  time.sleep(1)
  
def recv_string(client):
  return client.recv(2100).decode('utf-8')

def send_byte(client,message) :
  client.send(message)
  time.sleep(1)

def recv_byte(client) :
  return client.recv(2100)

def Register(client,myPrivatekey,ServerPublicKey) :
    print(recv_string(client))
    string=recv_string(client)
    while(string!="Input your password:"):
      print(string)
      username=input()
      username=encrypt_with_public_key(ServerPublicKey,username)
      send_byte(client,username)
      string=recv_string(client)
    print(string)
    password=input()
    password=encrypt_with_public_key(ServerPublicKey,password)
    send_byte(client,password)
    print(recv_string(client))
    email=input()
    email=encrypt_with_public_key(ServerPublicKey,email)
    send_byte(client,email)
    print(recv_string(client))

def Login(client,myPrivatekey,ServerPublicKey) :
  print(recv_string(client))
  string=recv_string(client)
  while(string!="Input your password:"):
    print(string)
    username=input()
    username=encrypt_with_public_key(ServerPublicKey,username)
    send_byte(client,username)
    string=recv_string(client)
  while string[0]=='I' or string[0]=='T' :
    print(string)
    if(string[0]=='Y') :
      exit()
    password=input()
    password=encrypt_with_public_key(ServerPublicKey,password)
    send_byte(client,password)
    string=recv_string(client)
  print(string)
  email=recv_byte(client)
  email=decrypt_with_private_key(myPrivatekey,email)
  print(email)

def Keyexchange(myPublickey,Client) :
    print("public key and private key generated")
    string=recv_string(Client)
    if string[0:5]=='prime' :
        prime=get_numbers(string)
        print("prime number is received")
    string=recv_string(Client)
    if string[0:9]=='generator' :
        generator=get_numbers(string)
        print("generator is received")
    string=recv_string(Client)
    if string[0:6]=='public' :
        print("get the interesting thing")
        heDiffieHellmanPublicKey=get_numbers(string)
        print("his DH public key is recieved")
    myDiffieHellmanPrivatekey = getgenerator_SK(prime)
    myDiffieHellmanPublickey = calculate_public_key(prime, generator, myDiffieHellmanPrivatekey)
    send_string(Client,"public key "+str(myDiffieHellmanPublickey))
    print("my DH public key is sent")
    sharedSecret=calculate_shared_secret(prime, heDiffieHellmanPublicKey, myDiffieHellmanPrivatekey)
    print("Diffie Hellman Exchange Finished")
    encrypted_publicKey=encrypt_with_aes(myPublickey.save_pkcs1().decode(),str(sharedSecret))
    Client.send(encrypted_publicKey)
    time.sleep(1)
    ServerPublicKey=rsa.PublicKey.load_pkcs1((decrypt_with_aes(Client.recv(2100),str(sharedSecret))).encode())
    print("Key Exchange Over")
    
    print("Shared secret is "+str(sharedSecret))
    
    return ServerPublicKey

Client = socket(AF_INET,SOCK_STREAM)
Client.connect(('127.0.0.1',8888))

myPublickey,myPrivatekey=generate_key_pair()
ServerPublicKey=Keyexchange(myPublickey,Client)
print("my public key is "+str(myPublickey.save_pkcs1().decode()))
print("Server public key is "+str(ServerPublicKey.save_pkcs1().decode()))

print(recv_string(Client))
string=input()
while string != "Register" and string != "Log in":
  print("Wrong Input! Please input Register or Login!")
  string=input()
send_string(Client,string)
if string == "Register" :
    Register(Client,myPrivatekey,ServerPublicKey)
Login(Client,myPrivatekey,ServerPublicKey)
    