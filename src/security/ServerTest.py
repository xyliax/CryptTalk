from socket import *
from Safe_Part import *
from Database_Part import *
from Socket_Transfer_Part import *

def Register(client,conn,myPrivatekey) :
    username=recv_byte(client)
    username=decrypt_with_private_key(myPrivatekey,username)
    if(check_member_exists(conn,username)):
        return 1 # username exists
    password=recv_byte(client)
    password=decrypt_with_private_key(myPrivatekey,password)
    email=recv_byte(client)
    email=decrypt_with_private_key(myPrivatekey,email)
    password=sha256_hash(password)
    email=encrypt_with_aes(email,'POLYU')
    add_data(conn,username,password.hex(),email.hex())
    return 0

def Login(client,conn,myPrivatekey,clientPublickey) :
    username=recv_byte(client)
    username=decrypt_with_private_key(myPrivatekey,username)
    if(check_member_exists(conn,username)==False):
        return 1 # username not exists
    password=recv_byte(client)
    password=decrypt_with_private_key(myPrivatekey,password)
    if(checkpassword(conn,username,sha256_hash(password).hex())==False):
        return 2 # wrong password
    email=bytes.fromhex(getemail(conn,username))
    email=decrypt_with_aes(email,'POLYU')
    email=encrypt_with_public_key(clientPublickey,email)
    client.send(email)
    return 0# login successfully
   
    
def Keyexchange(client) :
    myPublickey,myPrivatekey=generate_key_pair()
    prime=generate_prime_number()
    generator = getgenerator_SK(prime)
    myDiffieHellmanPrivatekey = getgenerator_SK(prime)
    myDiffieHellmanPublickey = calculate_public_key(prime, generator, myDiffieHellmanPrivatekey)
    send_string(client,"prime "+str(prime))
    send_string(client,"generator "+str(generator))
    send_string(client,"public key "+str(myDiffieHellmanPublickey))
    string=recv_string(client)
    if string[0:6]=='public' :
        heDiffieHellmanPublicKey=get_numbers(string)
    sharedSecret=calculate_shared_secret(prime, heDiffieHellmanPublicKey, myDiffieHellmanPrivatekey)
    encrypted_publicKey=encrypt_with_aes(myPublickey.save_pkcs1().decode(),str(sharedSecret))
    clientPublicKey=rsa.PublicKey.load_pkcs1((decrypt_with_aes(recv_byte(client),str(sharedSecret))).encode())
    send_byte(client,encrypted_publicKey)
    return myPrivatekey,myPublickey,clientPublicKey
    
def makeTable( ) :
    conn=createtable("database.db",'POLYU') 
    return conn

def serverSocket() :
    Server = socket(AF_INET,SOCK_STREAM)
    Server.bind(('127.0.0.1',8888))
    Server.listen()
    client,client_ip = Server.accept()
    return client


