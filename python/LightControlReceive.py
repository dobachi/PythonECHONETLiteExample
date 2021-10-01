import socket
import binascii

# https://qiita.com/f-paico/items/4104bc3ba7501ef57fa6 を参考に
# 動作確認するためのスクリプト

def receive_state():
    ECHONETport = 3610

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', ECHONETport))
    data, addr = sock.recvfrom(4096)

    # バイト列を16進数文字列に変換する
    data = str(binascii.hexlify(data), 'utf-8')
    print(data)


if __name__ == '__main__':
    receive_state()