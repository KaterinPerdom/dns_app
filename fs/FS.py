from flask import Flask
from flask import request
import logging as logi
import pickle as pk

import socket
app = Flask(__name__)

logi.basicConfig(format='[FS: %(asctime)s] %(message)s',
                datefmt='%I:%M:%S %p',
                level=logi.INFO)

@app.route('/')
def hello_world():
    return 'Hello Katerin! This is your Fibonnaci Server (FS)'

@app.route('/fibonacci')
def fibonacci():
    n = int(request.args.get('number'))
    logi.info(f"/fibonacci got n={n}")
    return str(calcfibonacci(n))

def calcfibonacci(n):
    if n < 0:
        print("Incorrect input")
    elif n == 0:
        return 0
    
    elif n ==1 or n==2:
        return 1
    else:
        return calcfibonacci(n - 1) + calcfibonacci(n - 2)

def register_as(as_ip, as_port, hostname, value, type, ttl):
    msg = ((hostname, value, type, ttl))
    msg_bytes = pk.dumps(msg)
    as_addr = (as_ip, as_port)
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    logi.info(f"Sending {msg} to {as_addr} via UDP socket")
    udp_socket.sendto(msg_bytes, as_addr)


@app.route('/register', methods=['PUT'])
def register():
    body = request.json
    logi.info(f"/register got body={body!r}")
    if not body:
        raise ValueError("There is no body")
    hostname = body["hostname"]
    fs_ip    = body["fs_ip"]
    as_ip    = body["as_ip"]
    as_port  = body["as_port"]
    ttl      = body["ttl"]
    register_as(as_port=as_port,
                     as_ip=as_ip,
                     hostname=hostname,
                     value=fs_ip,
                     type="A",
                     ttl=ttl)
    return "Great your registration Done!"
#UDP_IP = "127.0.0.1"
#UDP_PORT = 53533
#REGISTER_DICT = dict(hostname = "fibonacci.com", ip = "127.0.0.1")
#MESSAGE = "TYPE=A\nNAME="+REGISTER_DICT['hostname']+"\nVALUE="+REGISTER_DICT['ip']+"\nTTL=10"
 
#print("%s" % MESSAGE) 
#sock = socket.socket(socket.AF_INET, # Internet
#                      socket.SOCK_DGRAM) # UDP
#sock.sendto(MESSAGE.encode(),(UDP_IP, UDP_PORT))
#data, addr = sock.recvfrom(1024)
#reply = data.decode("utf-8")
#print(reply)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port= 9090,debug=True)