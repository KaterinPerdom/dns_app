from flask import Flask,request
import socket
import pickle as pk
import requests 
import json
import logging as logi


logi.basicConfig(format='[US: %(asctime)s] %(message)s',
                datefmt='%I:%M:%S %p',
                level=logi.INFO)
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello Katerin! This is your User Server (US)'


@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    hostname = request.args.get('hostname') 
    fs_port = (request.args.get('fs_port')) #UDP_PORT server
    number = int(request.args.get('number'))
    as_ip = request.args.get('as_ip')  #UDP_IP server AS
    as_port = int(request.args.get('as_port'))  #UDP_PORT server AS
    fs_ip = message_AS(hostname=hostname,as_ip=as_ip, as_port=as_port)
    
    if not fs_ip:
            code = 400
            msg = 'Bad Request'
            return msg, code
    else:
        return request.get(f"http://{fs_ip}:{fs_port}/fibonacci", params={"number": number}).content 


def message_AS(hostname, as_ip, as_port):
    logi.info(f"Getting FS {hostname!r} IP from AS {as_ip}:{as_port}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Message = pk.dumps(("A", hostname))
    sock.sendto(Message,(as_ip, as_port))
    response, _ = sock.recvfrom(1024)
    response = pk.loads(response)
    type, hostname, fs_ip, ttl = response
    logi.info(f"Resolved fs {hostname!r} to IP {fs_ip}")
    return fs_ip

app.run(host='0.0.0.0',port=8080, debug=True)

