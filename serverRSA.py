#server
import socket
import threading
import time

import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import MD5

#pubkey_client
#signature_client
 
# Use a larger key length in practice...
KEY_LENGTH = 1024  # Key size (in bits)
random_gen = Random.new().read

# Generate RSA private/public key pairs for server...
keypair_server = RSA.generate(KEY_LENGTH, random_gen)

# Public key export for exchange between parties...
pubkey_server  = keypair_server.publickey()	

# Plain text messages...
#message_to_pytn     = "Russia is really nice this time of year...\nUse encryption and make the NSA CPUs churn and burn!"

# Generate digital signatures using private keys...
#hash_of_pytn_message    = MD5.new(message_to_pytn).digest()
#signature_server       = keypair_server.sign(hash_of_pytn_message, '')

# Encrypt messages using the other party's public key...
#encrypted_for_pytn      = pubkey_pytn.encrypt(message_to_pytn, 32)          #from Server

# Decrypt messages using own private keys...
#decrypted_server   = keypair_server.decrypt(encrypted_for_server)

# Signature validation and console output...
#hash_server_decrypted = MD5.new(decrypted_server).digest()
#if pubkey_pytn.verify(hash_server_decrypted, signature_pytn):
    #print "Server received from Client:"
    #print decrypted_server
    #print ""

SIZE = 4

soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
soc.bind(('127.0.0.1',5432))
soc.listen(5)

class CThread(threading.Thread):
    def __init__(self,c):
        threading.Thread.__init__(self)
        self.conn = c
        self.stopIt=False

    def mrecv(self):
        data = self.conn.recv(SIZE)
        self.conn.send('OK')
        msg = self.conn.recv(int(data))
        return msg

    def run(self):
        while not self.stopIt:
            msg = self.mrecv()
            print 'recieved->  ',msg

def setConn(con1,con2):
    dict={}
    state = con1.recv(9)
    con2.recv(9)
    if state =='WILL RECV':
        dict['send'] = con1 # server will send data to reciever
        dict['recv'] = con2
    else:
        dict['recv'] = con1 # server will recieve data from sender
        dict['send'] = con2
    return dict

def msend(conn,msg):
    if len(msg)<=999 and len(msg)>0:
        conn.send(str(len(msg)))
        if conn.recv(2) == 'OK':
            conn.send(msg)
    else:
        conn.send(str(999))
        if conn.recv(2) == 'OK':
            conn.send(msg[:999])
            msend(conn,msg[1000:]) # calling recursive


(c1,a1) = soc.accept()
(c2,a2) = soc.accept()
dict = setConn(c1,c2)
thr = CThread(dict['recv'])
thr.start()
try:
    while 1:
        msend(dict['send'],raw_input())
except:
    print 'closing'
thr.stopIt=True
msend(dict['send'],'bye!!!')# for stoping the thread
thr.conn.close()
soc.close()
