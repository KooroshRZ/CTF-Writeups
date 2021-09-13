from Crypto.Util.number import *
from hashlib import sha1
import re
import socket
from time import sleep

host = "185.235.41.166"
port = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

while True:
    sleep(15)

    data = sock.recv(2048).decode()
    print(data)

    q = int(re.search(r'q = (.*)\n', data).group(1))

    messages = re.findall(r"sign\('(.*)'\)", data)
    m1 = messages[0]
    m2 = messages[1]


    signatures = re.findall(r"'\) = (.*)\n", data)
    s1 = int(signatures[0])
    s2 = int(signatures[1])


    s = int(re.findall(r"sign\(secret\) = (.*) (.*)", data)[0][0])
    r = int(re.findall(r"sign\(secret\) = (.*) (.*)", data)[0][1])

    hm1 = int(sha1(m1.encode('utf-8')).hexdigest(), 16)
    hm2 = int(sha1(m2.encode('utf-8')).hexdigest(), 16)

    ds = s2 - s1
    dm = hm2 - hm1

    k = (inverse(ds, q) * dm) % q

    x = ((s1*k - hm1) * inverse(r, q)) % q

    m = (s*k - x*r) % q
    print(m)

    sock.sendall(str(m).encode() + b"\n")
    sleep(5)
    info = sock.recv(2048).decode()
    print(info)
