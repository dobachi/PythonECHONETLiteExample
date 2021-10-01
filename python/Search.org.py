#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://end0tknr.hateblo.jp/entry/20170305/1488712308 を参考にした。

import asyncore
import codecs
import netifaces
import socket
import threading
from time import sleep

UDP_RESES = []
UDP_PORT = 3610 # for UDP

def main():
    # 自身のipアドレスを探索
    local_ip = UdpSender.find_local_ip_addr()
    if local_ip == None:
        return None
    
    # echonetのコマンドをudp送信
    sender = UdpSender(local_ip)

    echonet_cmd = echonet_cmd_ls() ##echonet機器の一覧取得用コマンド生成

    # 224.0.23.0 とは、ECHONET専用のマルチキャストアドレス
    sender.send_msg("224.0.23.0", echonet_cmd)
    # sender.send_msg("10.0.4.73", echonet_cmd)

## http://qiita.com/miyazawa_shi/items/725bc5eb6590be72970d
def echonet_cmd_ls():
 
    cmd_cols = ["1081",   ## echonetであることの宣言
                "0000",   ## 自由欄
                "05ff01", ## SEOJ(送信元機器) 05ff01=コントローラ
                "0ef001", ## DEOJ(送信先機器) 0ef001=ノード
                "62",     ## 60=set, 61=set(要:応答), 62=get
                "01",     ## 処理プロパティ数
                "d6",     ## プロパティ名 d6=自ノードlist.
                          ## https://echonet.jp/spec_v112_lite/ にある
                          ## 第2部 ECHONET Lite 通信ミドルウェア仕様の
                          ## 6.11.1 ノードプロファイル詳細規定 参照
               "00"]
    echonet_cmd = "".join(cmd_cols)
    return echonet_cmd

class UdpSender():
    def __init__(self, local_ip):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.IPPROTO_IP,
                             socket.IP_MULTICAST_IF,
                             socket.inet_aton(local_ip))
        
    def send_msg(self, ip,message):
        decode_hex = codecs.getdecoder("hex_codec")
        msg = decode_hex( message )[0]
        print('send!')
        self.sock.sendto(msg, (ip, UDP_PORT))

    def close(self):
        self.sock.close()

    @staticmethod
    def find_local_ip_addr(find_iface_name=None):
        for iface_name in netifaces.interfaces():
            iface_data = netifaces.ifaddresses(iface_name)
            af_inet = iface_data.get(netifaces.AF_INET)
        
            if not af_inet: continue

            ip_addr = af_inet[0]["addr"]
            
            if find_iface_name == None:
                return ip_addr
            elif iface_name == find_iface_name:
                return ip_addr
        return None

if __name__ == '__main__':
    main()