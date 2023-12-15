from socket import *
from Safe_Part import *
from Database_Part import *
def send_string(client, message):
  client.send(bytes(message, encoding='utf-8'))
  
def recv_string(client):
  return client.recv(1024).decode('utf-8')

dbname="database.db"
encryption_Password="POLYU"

def Register(client,conn) :
    send_string(client,"Register Part")
    send_string(client,"Input your username:")
    while(1) :
        username=recv_string(client)
        if(check_member_exists(conn,username,password)):
            send_string(client,"The username has been used! Input again!")
            continue
        else :
            break
    send_string(client,"Input your password:")
    password=recv_string(client)
    send_string(client,"Input your email:")
    email=recv_string(client)
    
    password=sha256_hash(password)
    email=encrypt_with_aes(email,encryption_Password)
    add_data(conn,username,password,email)
    send_string(client,"Register successfully!")

def Login(client,conn) :
    send_string(client,"Log in Part")
    send_string(client,"Input your username:")
    while(1) :
        username=recv_string(client)
        if(check_member_exists(conn,username)==False):
            send_string(client,"The username does not exist! Input again!")
            continue
        else :
            break
    email=getemail(conn,username)
    send_string(client,"You can check the identity of our server by the following information: your email is "+decrypt_with_aes(email,encryption_Password))
    times=0
    while(1):
        if(times==3):
            send_string(client,"You have input the wrong password for three times! Please try again later!")
            client.close()
            Server.close()
            exit()
        send_string(client,"Input your password:")
        password=recv_string(client)
        if(checkpassword(conn,username,sha256_hash(password))==False):
            send_string(client,"The password is wrong! Input again!")
            times+=1
            continue
        else :
            break
    send_string(client,"Log in successfully!")
    
myPublickey,myPrivatekey=generate_key_pair()
conn=create_connection(dbname,encryption_Password) 
# connect to the database, if the database does not exist, it will create a new one
Server = socket(AF_INET,SOCK_STREAM)
Server.bind('127.0.0.1',8888)
Server.listen()
client,client_ip = Server.accept()

send_string(client,"Input Register or Log in!")
string=recv_string(client)
if string == "Register":
    Register(client,conn)
    string="Log in"
if string == "Log in":
    Login(client,conn)

