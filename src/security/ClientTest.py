from socket import *
from Safe_Part import *
from Socket_Transfer_Part import *
from Socket_Transfer_Part import *

def Register(client,ServerPublicKey,username,password,email) :
   
    username=encrypt_with_public_key(ServerPublicKey,username)
    send_byte(client,username)
    password=encrypt_with_public_key(ServerPublicKey,password)
    send_byte(client,password)
    email=encrypt_with_public_key(ServerPublicKey,email)
    send_byte(client,email)

def Login(client,myPrivatekey,ServerPublicKey,username,password) :
    username=encrypt_with_public_key(ServerPublicKey,username)
    send_byte(client,username)
    password=encrypt_with_public_key(ServerPublicKey,password)
    send_byte(client,password)
    email=recv_byte(client)
    email=decrypt_with_private_key(myPrivatekey,email)
    return email

def Keyexchange(myPublickey,Client) :
    myPublickey,myPrivatekey=generate_key_pair()
    
    string=recv_string(Client)
    if string[0:5]=='prime' :
        prime=get_numbers(string)
    string=recv_string(Client)
    if string[0:9]=='generator' :
        generator=get_numbers(string)
    string=recv_string(Client)
    if string[0:6]=='public' :
        heDiffieHellmanPublicKey=get_numbers(string)
    myDiffieHellmanPrivatekey = getgenerator_SK(prime)
    myDiffieHellmanPublickey = calculate_public_key(prime, generator, myDiffieHellmanPrivatekey)
    send_string(Client,"public key "+str(myDiffieHellmanPublickey))
    sharedSecret=calculate_shared_secret(prime, heDiffieHellmanPublicKey, myDiffieHellmanPrivatekey)
    encrypted_publicKey=encrypt_with_aes(myPublickey.save_pkcs1().decode(),str(sharedSecret))
    send_byte(Client,encrypted_publicKey)
    ServerPublicKey=rsa.PublicKey.load_pkcs1((decrypt_with_aes(recv_byte(Client),str(sharedSecret))).encode())

    return myPrivatekey,myPublickey,ServerPublicKey
def clientSocket( ) :
    Client = socket(AF_INET,SOCK_STREAM)
    Client.connect(('127.0.0.1',8888))
    return Client

