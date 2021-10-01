#!/usr/bin/env python

# https://chakoku.hatenablog.com/entry/2020/11/14/115043 を
# 参考に試してみる例
# そのほか、 https://end0tknr.hateblo.jp/entry/20170305/1488712308 も参考にした。

#!/usr/bin/python3
# original source:
# https://memo.saitodev.com/home/python_network_programing/#id5

import socket
import netifaces

PORT = 3610
bufsize = 1024

MULTICAST_GROUP='224.0.23.0'

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

def parse_echonet_res(echonet_res_orig):
    echonet_res = [hex(x) for x in echonet_res_orig]
    res_cols = [echonet_res[ 0: 2],  ## echonetであることの宣言
                echonet_res[ 2: 4],  ## 自由欄
                echonet_res[ 4: 7],  ## SEOJ(送信元機器) 0ef001=ノード
                echonet_res[ 7:10],  ## DEOJ(送信先機器) 05ff01=コントローラ
                echonet_res[10:11],  ## 応答code. 71=set 72=get
                echonet_res[11:12],  ## 処理プロパティ数 1
                echonet_res[12:13],  ## EPC. プロパティ名 d6 自ノードインスタンスリストS
                echonet_res[13:14],  ## PDC. 後のbyte数 4
                echonet_res[14:]   ## EDT (例：0x1 -> 総数1、インスタンス010301。MoekadenRoomだと6個)
                ]
    return res_cols

def main():
    # 自身のipアドレスを探索
    local_ip = find_local_ip_addr()
    if local_ip == None:
        return None

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', PORT))
    # マルチキャストとユニキャストの両方を待ち受け
    sock.setsockopt(socket.IPPROTO_IP,
                    socket.IP_ADD_MEMBERSHIP,
                    socket.inet_aton(MULTICAST_GROUP) + socket.inet_aton(local_ip))

    while True:
      data = sock.recvfrom(bufsize)
      echonet_res = parse_echonet_res(data[0])
      print('# original')
      print(data)
      print('# parsed')
      print(echonet_res)

    sock.close()

if __name__ == '__main__':
    main()