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

dbname="database.db"
encryption_Password="POLYU"

def Register(client,conn,myPrivatekey,clientPublickey) :
    send_string(client,"Register Part")
    send_string(client,"Input your username:")
    while(1) :
        username=recv_byte(client)
        username=decrypt_with_private_key(myPrivatekey,username)
        if(check_member_exists(conn,username)):
            send_string(client,"The username has been used! Input again!")
            continue
        else :
            break
    send_string(client,"Input your password:")
    password=recv_byte(client)
    password=decrypt_with_private_key(myPrivatekey,password)
   
    send_string(client,"Input your email:")
    email=recv_byte(client)
    email=decrypt_with_private_key(myPrivatekey,email)
    password=sha256_hash(password)
    email=encrypt_with_aes(email,encryption_Password)
    
    add_data(conn,username,password.hex(),email.hex())
    send_string(client,"Register successfully!")

def Login(client,conn,myPrivatekey,clientPublickey) :
    send_string(client,"Log in Part")
    send_string(client,"Input your username:")
    while(1) :
        username=recv_byte(client)
        username=decrypt_with_private_key(myPrivatekey,username)
        print(username)
        if(check_member_exists(conn,username)==False):
            send_string(client,"The username does not exist! Input again!")
            continue
        else :
            break
    times=0
    while(1):
        if(times==3):
            send_string(client,"You have input the wrong password for three times! Please try again later!")
            exit()
        send_string(client,"Input your password:")
        password=recv_byte(client)
        password=decrypt_with_private_key(myPrivatekey,password)
        if(checkpassword(conn,username,sha256_hash(password).hex())==False):
            send_string(client,"The password is wrong! Input again!")
            times+=1
            continue
        else :
            break
    email=bytes.fromhex(getemail(conn,username))
    email=decrypt_with_aes(email,encryption_Password)
    email=encrypt_with_public_key(clientPublickey,email)
    send_string(client,"Log in successfully! You can check the identity of our server by the following information: your email is ")
    client.send(email)
    time.sleep(1)
   
    
def Keyexchange(myPublickey,client,) :
    print("public key and private key generated")
    prime=generate_prime_number()
    generator = getgenerator_SK(prime)
    myDiffieHellmanPrivatekey = getgenerator_SK(prime)
    myDiffieHellmanPublickey = calculate_public_key(prime, generator, myDiffieHellmanPrivatekey)
    send_string(client,"prime "+str(prime))
    print("prime is sent")
    send_string(client,"generator "+str(generator))
    print("generator is sent")
    send_string(client,"public key "+str(myDiffieHellmanPublickey))
    print("my DH public key is sent")
    string=recv_string(client)
    if string[0:6]=='public' :
        heDiffieHellmanPublicKey=get_numbers(string)
        print("his DH public key is recieved")
    sharedSecret=calculate_shared_secret(prime, heDiffieHellmanPublicKey, myDiffieHellmanPrivatekey)
    print("Diffie Hellman Exchange Finished")
    encrypted_publicKey=encrypt_with_aes(myPublickey.save_pkcs1().decode(),str(sharedSecret))
    clientPublicKey=rsa.PublicKey.load_pkcs1((decrypt_with_aes(client.recv(2100),str(sharedSecret))).encode())
    client.send(encrypted_publicKey)
    time.sleep(1)
    print("Key Exchange Over")
    
    print("Shared secret is "+str(sharedSecret))
    
    return clientPublicKey
    
    
conn=createtable(dbname,encryption_Password) 
# connect to the database, if the database does not exist, it will create a new one
Server = socket(AF_INET,SOCK_STREAM)
Server.bind(('127.0.0.1',8888))
Server.listen()
client,client_ip = Server.accept()
myPublickey,myPrivatekey=generate_key_pair()
clientPublickey=Keyexchange(myPublickey,client)

print("my public key is "+str(myPublickey.save_pkcs1().decode()))
print("Client public key is "+str(clientPublickey.save_pkcs1().decode()))

send_string(client,"Input Register or Log in!")
string=recv_string(client)
if string == "Register":
    Register(client,conn,myPrivatekey,clientPublickey)

Login(client,conn,myPrivatekey,clientPublickey)

