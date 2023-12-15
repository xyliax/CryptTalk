from socket import *
from Safe_Part import *
from Database_Part import *
def send_string(client, message):
  client.send(bytes(message, encoding='utf-8'))
  
def recv_string(client):
  return client.recv(1024).decode('utf-8')

dbname="database.db"
password="POLYU"
conn=create_connection(dbname,password) 
# connect to the database, if the database does not exist, it will create a new one
Server = socket(AF_INET,SOCK_STREAM)
Server.bind('127.0.0.1',8888)
Server.listen()
client,client_ip = Server.accept()

send_string(client,"Input Register or Log in!")
string=recv_string(client)
if string == "Register":
    while(1) :
        send_string(client,"Input your username:")
        username=recv_string(client)
        if((conn,username)):
            send_string(client,"The username has been used! Input again!")
            continue
    send_string(client,"Input your password:")
    password=recv_string(client)
    send_string(client,"Input your email:")
    email=recv_string(client)
    add_data(conn,username,password,email)
    send_string(client,"Register successfully!")
