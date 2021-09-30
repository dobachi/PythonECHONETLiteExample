import socket
import binascii

def receive_state():
    ECHONETport = 3610

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', ECHONETport))
    data, addr = sock.recvfrom(4096)

    # バイト列を16進数文字列に変換する
    data = str(binascii.hexlify(data), 'utf-8')
    print(data)


if __name__ == '__main__':
    receive_state()