import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import long_to_bytes,bytes_to_long
from time import sleep

HOST = '178.62.109.113'
PORT = 32663
BLOCK_SIZE = 32

flag_size = 25

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

data = s.recv(4096).decode()
print(data)

prefix = b'00'*4
flag = b''
sleep(2)
index = 0

while True:
    for i in range(32,127):

        sleep(1)
        tmp = chr(i).encode() + flag
        tmp = pad(tmp, BLOCK_SIZE//2).hex().encode()
        tmp = prefix + tmp + index*b'00' + 8*b'00'
        # print(tmp)
        s.sendall(tmp)
        sleep(1)

        data = s.recv(4096).decode().rstrip()
        blocks = [data[i:i+BLOCK_SIZE] for i in range(0, len(data), BLOCK_SIZE)]

        if blocks[1] == blocks[4+(index//15)]:
            flag = chr(i).encode() + flag
            index += 1
            print(flag.decode())
            break

