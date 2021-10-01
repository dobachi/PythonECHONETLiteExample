import socket
import binascii
from threading import Thread
import time
import sys

# https://qiita.com/f-paico/items/4104bc3ba7501ef57fa6 を参考に
# 動作確認するためのスクリプト

def light_switch(host, command):
    if command == 'on':
        prop = '30'
    elif command == 'off':
        prop = '31'
    else:
        prop = '31'
        
    ip = '10.0.4.73'
    # ECHONET LiteはUDPの3610番ポートを使用する
    ECHONETport = 3610
    format_echonet_lite = ['EHD', 'TID', 'SEOJ', 'DEOJ', 'ESV', 'OPC', 'EPC', 'PDC', 'EDT']
    data_format = {
        format_echonet_lite[0]: '1081',
        format_echonet_lite[1]: '0000',
        format_echonet_lite[2]: '05FF01',
        format_echonet_lite[3]: '029001',
        format_echonet_lite[4]: '61',  # 応答を受け取る
        format_echonet_lite[5]: '01',
        format_echonet_lite[6]: '80',
        format_echonet_lite[7]: '01',
        format_echonet_lite[8]: prop
    }

    frame = ''
    for key in format_echonet_lite:
        frame += data_format[key]

    # 16進数文字列をバイト列に変換する
    msg = binascii.unhexlify(frame)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg, (host, ECHONETport))
    print('send %s to %s' % (command, host))

if __name__ == '__main__':
    args = sys.argv
    light_switch(args[1], args[2]);