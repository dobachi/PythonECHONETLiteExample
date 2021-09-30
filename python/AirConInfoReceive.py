#!/usr/bin/env python

# https://yomon.hatenablog.com/entry/2020/09/sharp_aircon_echonet_lite を
# 参考に試してみる例

import socket

def receive():
    echonet_port = 3610
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_sock.bind(("0.0.0.0", echonet_port))
    
    data, addr = recv_sock.recvfrom(1024)
    for index, value in enumerate(data):
        print('%s: %s' % (index, hex(value)))
        
    print(addr)
    recv_sock.close()

if __name__ == '__main__':
    receive()