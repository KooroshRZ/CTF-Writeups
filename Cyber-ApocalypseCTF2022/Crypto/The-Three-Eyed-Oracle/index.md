# Challenge code

```py
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import random
import signal
import subprocess
import socketserver

FLAG = b'HTB{--REDACTED--}'
prefix = random.randbytes(12)
key = random.randbytes(16)

def encrypt(key, msg):
    msg = bytes.fromhex(msg)
    crypto = AES.new(key, AES.MODE_ECB)
    padded = pad(prefix + msg + FLAG, 16)
    return crypto.encrypt(padded).hex()


def challenge(req):
    req.sendall(b'Welcome to Klaus\'s crypto lab.\n' +
                b'It seems like there is a prefix appended to the real firmware\n' +
                b'Can you somehow extract the firmware and fix the chip?\n')
    while True:
        req.sendall(b'> ')
        try:
            msg = req.recv(4096).decode()

            ct = encrypt(key, msg)
        except:
            req.sendall(b'An error occurred! Please try again!')

        req.sendall(ct.encode() + b'\n')


class incoming(socketserver.BaseRequestHandler):
    def handle(self):
        signal.alarm(1500)
        req = self.request
        challenge(req)


class ReusableTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


def main():
    socketserver.TCPServer.allow_reuse_address = True
    server = ReusableTCPServer(("0.0.0.0", 1337), incoming)
    server.serve_forever()


if __name__ == "__main__":
    main()
```

# Solution
we have an oracle that gets the message from us and encrypts it in this way\
It adds a random fixed prefix before the message and then adds the Flag after it and encrypts the whole data.

```py
msg = bytes.fromhex(msg)
crypto = AES.new(key, AES.MODE_ECB)
padded = pad(prefix + msg + FLAG, 16)
```


The problem is that it uses ECB mode which stands for (Electronic Code Book). The problem with this mode is that the same message block will result in the same encrypted block. We can abuse this feature plus controlling the msg we send to the server in a way that we can decrypt the encrypted flag.
According to this [link](https://crypto.stackexchange.com/questions/42891/chosen-plaintext-attack-on-aes-in-ecb-mode) for example we wanna determine the last character of the flag which is }.
The message we should send is like this

```py
i = "chr(})"
prefix = b'00'*4
flag = b''
tmp = chr(i).encode() + flag
tmp = pad(tmp, BLOCK_SIZE).hex().encode()
tmp = prefix + tmp + index*b'00' + 8*b'00'
# we should brute force 8 number to find what length tha flag has
# it should be (length of the flag) % (block_size+1) and here we got 8 
# which means flag size is 25 chars


# tmp will be
'00000000' -> 4 null bytes prefix to end previous 12 prefix block
'7d0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f' -> last flag character plus padding
'0000000000000000' -> extra characters to ensure
last character of flag will be first character of final block

after sending this payload the message at the server looks like this

1st BLock: 12 bytes random fixed prefix + '00000000' 
2nd BLock: '7d0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f' -> '}...............'
3rd Block: '0000000000000000' + flag[0:8]
4th Block: flag[8:24]
5th Block: padded(flag[24])
           -> '7d0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f' -> '}...............
```

Here we see that blocks 2 and 5 are exactly the same containing the last character of the flag so if we see the same encrypted block in output(because it's ECB mode) then we can confirm that the length of the flag is 25 and the ending character. as we can see blocks 2,5 are the same.

```
echo '3c352942c46f278ddc0256fca5a8a5b17b735f447a1412d5200b7ae1d66035a44b57a6dae02293bbed038aa2566e764b1f71fac5c2146e56c89
5b6d42fbebf457b735f447a1412d5200b7ae1d66035a44b57a6dae02293bbed038aa2566e764b' | xxd -p -r | xxd                                                                                                                   
00000000: 3c35 2942 c46f 278d dc02 56fc a5a8 a5b1  <5)B.o'...V.....                                                                                                                                                
00000010: 7b73 5f44 7a14 12d5 200b 7ae1 d660 35a4  {s_Dz... .z..`5.                                                                                                                                                
00000020: 4b57 a6da e022 93bb ed03 8aa2 566e 764b  KW..."......VnvK                                                                                                                                                
00000030: 1f71 fac5 c214 6e56 c895 b6d4 2fbe bf45  .q....nV..../..E                                                                                                                                                
00000040: 7b73 5f44 7a14 12d5 200b 7ae1 d660 35a4  {s_Dz... .z..`5.                                                                                                                                                
00000050: 4b57 a6da e022 93bb ed03 8aa2 566e 764b  KW..."......VnvK                                                                                                                                                
```

We should Bruteforce each character and add the required padding to find each character. Here is the automated code to find each character of the flag

```py
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
```

And after waiting for a few minutes 

```
kourosh@kryptonz:~/ctf$ python3.8 solve.py                                                                                                                                                                         
Welcome to Klaus's crypto lab.                                                                                                                                                                                     
It seems like there is a prefix appended to the real firmware                                                                                                                                                      
Can you somehow extract the firmware and fix the chip?                                                                                                                                                             
                                                                                                                                                                                                                   
}                                                                                                                                                                                                                  
y}                                                                                                                                                                                                                 
ry}                                                                                                                                                                                                                
3ry}                                                                                                                                                                                                               
v3ry}                                                                                                                                                                                                              
0v3ry}                                                                                                                                                                                                             
c0v3ry}                                                                                                                                                                                                            
3c0v3ry}                                                                                                                                                                                                           
r3c0v3ry}                                                                                                                                                                                                          
_r3c0v3ry}                                                                                                                                                                                                         
7_r3c0v3ry}                                                                                                                                                                                                        
37_r3c0v3ry}                                                                                                                                                                                                       
r37_r3c0v3ry}                                                                                                                                                                                                      
cr37_r3c0v3ry}                                                                                                                                                                                                     
3cr37_r3c0v3ry}                                                                                                                                                                                                    
53cr37_r3c0v3ry}                                                                                                                                                                                                   
_53cr37_r3c0v3ry}                                                                                                                                                                                                  
y_53cr37_r3c0v3ry}                                                                                                                                                                                                 
5y_53cr37_r3c0v3ry}                                                                                                                                                                                                
45y_53cr37_r3c0v3ry}                                                                                                                                                                                               
345y_53cr37_r3c0v3ry}                                                                                                                                                                                              
{345y_53cr37_r3c0v3ry}
B{345y_53cr37_r3c0v3ry}
TB{345y_53cr37_r3c0v3ry}
HTB{345y_53cr37_r3c0v3ry}
```

The flag
```
HTB{345y_53cr37_r3c0v3ry}
```

[solution code](https://github.com/KooroshRZ/CTF-Writeups/blob/main/ApocalypseCTF2022/Crypto/The-Three-Eyed-Oracle/solve.py)
<br>
> KouroshRZ for **AbyssalCruelty**

