import logging as logi
import socket
import json
import os
import time 
import pickle as pk


UDP_IP = "0.0.0.0"
UDP_PORT = 53533

TYPE = "A"

logi.basicConfig(format='[%(asctime)s %(filename)s:%(lineno)d] %(message)s',
                datefmt='%I:%M:%S %p',
                level=logi.DEBUG)

def dns_record(name):
    FILE = "data.json"
    with open(FILE, 'r') as outfile:
        register_exit = json.load(outfile)
    if name not in register_exit:
        logi.info(":( NO DNS record found for {NAME}")
        return
        
def parsemessage(name, value, type, ttl):
    FILE = "data.json"
    if not os.path.exists(FILE):
        with open(FILE, 'w') as outfile:
            json.dump({}, outfile , indent= 4)
        
    with open(FILE, 'r') as outfile:
        register_exit = json.load(outfile)
        
    ttl_ts = time.time() + ttl
    register_exit[name] = (value, ttl_ts, ttl)

    with open(FILE, 'w') as outfile:
        json.dump(register_exit, outfile, indent =3)
        logi.debug(f"Okay! Saving DNS record for {name} {(value, ttl)}")
    
    value, ttl_ts, ttl = register_exit[name]
    logi.debug(f"Got DNS records for {name}: {register_exit[name]}")
    #If the time is greater that TTL, our register expired :(
    logi.debug(f"Curr time={time.time()} ttl_ts={ttl_ts}")
    if time.time() > ttl_ts:
        logi.info(f"TTL expired for follow {name}")
        return None
    return (TYPE, name, value, ttl_ts, ttl)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))
    logi.info(f"The UDP server is up and running, and it is listening: " f"{socket.gethostbyname(socket.gethostname())}:{UDP_PORT}")

    while 1:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        message = pk.loads(data)            #print("received message: %s" % data.decode())
        logi.info(f"Message from Client: {message!r}")
        if len(message) == 4:
            name, value, type , ttl = pk.loads(data)
            parsemessage(name=name, type =type, value =value, ttl=ttl)
        elif len(message) == 2:
            type, name = message
            record_dns = dns_record(name)
            if record_dns:
                (_, name, value, _, ttl) = record_dns
                response = (type, name, value, ttl)
            else:
                response = ""
            msg_response_bytes = pk.dumps(response)
            sock.sendto(msg_response_bytes, addr)
        else:
            message = f"Expected msg of len 4 or 2, got :{message!r}"
            logi.error(message)
            data.sendto(message, addr)

if __name__ == '__main__':
    logi.info("Authoritative server")
    main()