import binascii
import hashlib
import sys
from Crypto.Cipher import AES
from Crypto.Util.number import *

gkey = '*XhN2*8d%8Slp3*v'
key_len = len(gkey)

def repeating_xor_key(cip: bytes, key: bytes) -> bytes:

    repeation = 1 + (len(cip) // len(key))
    key = key * repeation
    key = key[:len(cip)]
    
    msg = bytes([c ^ k for c, k in zip(cip, key)])
    return msg

def pad(message):
    padding = bytes((key_len - len(message) % key_len) * chr(key_len - len(message) % key_len), encoding='utf-8')
    return message + padding


def brute_key():

    key = gkey
    check = bytes.fromhex('9f43fd6634')
    
    for i in range(0, 256):

        tindex1 = key.find('*')
        key = key.replace('*', chr(i), 1)

        for j in range(0, 256):

            tindex2 = key.find('*')
            key = key.replace('*', chr(j), 1)

            for k in range(0, 256):

                tindex3 = key.find('*')
                key = key.replace('*', chr(k), 1)

                h = hashlib.sha256(key.encode("latin")).hexdigest()
                hidden = binascii.unhexlify(h)[:10]

                message =  b'CBC (Cipher Blocker Chaining) is an advanced form of block cipher encryption'
                message += hidden
                m = pad(message)

                c1 = bytes.fromhex('1f3ef3fab2bbfc838b9ef71867c3bcbb')
                b1 = m[-16:]

                aes = AES.new(key.encode("latin"), AES.MODE_ECB)
                c2 = repeating_xor_key(aes.decrypt(c1), b1)

                if (c2[-5:] == check):
                    print(key)
                    return key

                tlist3 = list(key)
                tlist3[tindex3] = "*"
                key = "".join(tlist3)

            tlist2 = list(key)
            tlist2[tindex2] = "*"
            key = "".join(tlist2)

        tlist1 = list(key)
        tlist1[tindex1] = "*"
        key = "".join(tlist1)


def find_IV(key):

    h = hashlib.sha256(key.encode("latin")).hexdigest()
    hidden = binascii.unhexlify(h)[:10]

    message =  b'CBC (Cipher Blocker Chaining) is an advanced form of block cipher encryption'
    message += hidden
    message = pad(message)

    cipher = bytes.fromhex('1f3ef3fab2bbfc838b9ef71867c3bcbb')
    block = message[-16:]
    
    for i in range(2, 8):

        print("*"*50)
        print(hex(bytes_to_long(cipher)))
        aes = AES.new(key.encode("latin"), AES.MODE_ECB)
        cipher = repeating_xor_key(aes.decrypt(cipher), block)
        block = message[i*-16:(i-1)*-16]
        print(cipher)
        
key = brute_key()
find_IV(key)