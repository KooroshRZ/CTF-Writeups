from Crypto.Util.number import *
import requests
from time import sleep
from base64 import b64decode, b64encode

e = 65537
n = 18715011074845201888461791635367939553127268741525950569055646875583327021443659607353245335187865361831529174071669661800528518176785167923308382984980321847478987926576247803348565556467000769050253772844145294990007795239704368742758715638684197107821145503822208902630562212196150687206173690351749551186916854004800008749003363909832293560576767718140701898004524379681439118806637039874040392205378664659395484677831078036091366325220167320887257243286797974984343134558810336555940238652681956118161528469286073332846230059435703156764997667143302728650989754913668998360685694621902578380578148606411339422571
enc = b64decode("dOBQEtYlozOcFweWVnH1tz0ju295tVXP0E6/tvlWN6jtNR51fQjO7D3Up6BIijSuZvW20eE5O4LVoRlBTQKwttHI2ND9Pe0xw1wkeca2LweKtQgJD0BMnmdXDiOtrnWRGmY9Iz1gG+atU4PriO7Nunk/xluqv1r5gZFBAO/uTCzAfJ4vjH1LxXRLHmSIaZkTJpNtdglXm/Ve9w0UXijzGZItphRdaZ4PSkKGBuN2Az7AxoyFRQWgRzCh1+fua29628eVHlcgoif9mcD2+1KV7KYLw28e6qyv4t3HpOwl+9H1BYAzsJkZVmk/9bQuyjLVjLfcceVKiRI79MZn3FQ11g==")

def encrypt(m):

    url = "https://ugupugu.roboepics.com/encrypt"

    resp = requests.post(url, data=m)
    data = resp.content
    return b64decode(data)

def decrypt(c):

    url = "https://ugupugu.roboepics.com/decrypt"

    resp = requests.post(url, data=b64encode(c))
    data = resp.content
    return bytes_to_long(data)


c2 = bytes_to_long(encrypt("\x02"))
ct = c2 * bytes_to_long(enc) % n

flag = ( decrypt(long_to_bytes(ct)) * inverse(2, n) ) % n
print(long_to_bytes(flag))
