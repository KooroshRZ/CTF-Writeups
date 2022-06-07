# rsa

## challenge info
Using this command we get challenge info
```bash
xero ch show rsa

     Ugupugu

# overview

Decrypt this string, read the result text and retrieve the flag from it:
"dOBQEtYlozOcFweWVnH1tz0ju295tVXP0E6/tvlWN6jtNR51fQjO7D3Up6BIijSuZvW20eE5O4LVoRlBTQKwttHI2ND9Pe0xw1wkeca2LweKtQgJD0BMnmdXDiOtrnWRGmY9Iz1gG+atU4PriO7Nunk/xluqv1r5gZFBAO/uTCzAfJ4vjH1LxXRLHmSIaZkTJpNtdglXm/Ve9w0UXijzGZItphRdaZ4PSkKGBuN2Az7AxoyFRQWgRzCh1+fua29628eVHlcgoif9mcD2+1KV7KYLw28e6qyv4t3HpOwl+9H1BYAzsJkZVmk/9bQuyjLVjLfcceVKiRI79MZn3FQ11g=="
using: https://ugupugu.roboepics.com
```

we have a cipher text in b64 format and also a link `https://ugupugu.roboepics.com`\
decoding base64 does not reveal any information except for the length of the decoded message which is 256 bytes so according to the challenge name it's RSA and the modulus length would be `256*8 = 2048` bit
```bash
echo "dOBQEtYlozOcFweWVnH1tz0ju295tVXP0E6/tvlWN6jtNR51fQjO7D3Up6BIijSuZvW20eE5O4LVoRlBTQKwttHI2ND9Pe0xw1wkeca2LweKtQgJD0BMnmdXDiOtrnWRGmY9Iz1gG+atU4PriO7Nunk/xluqv1r5gZFBAO/uTCzAfJ4vjH1LxXRLHmSIaZkTJpNtdglXm/Ve9w0UXijzGZItphRdaZ4PSkKGBuN2Az7AxoyFRQWgRzCh1+fua29628eVHlcgoif9mcD2+1KV7KYLw28e6qyv4t3HpOwl+9H1BYAzsJkZVmk/9bQuyjLVjLfcceVKiRI79MZn3FQ11g==" | base64 -d | xxd

00000000: 74e0 5012 d625 a333 9c17 0796 5671 f5b7  t.P..%.3....Vq..
00000010: 3d23 bb6f 79b5 55cf d04e bfb6 f956 37a8  =#.oy.U..N...V7.
00000020: ed35 1e75 7d08 ceec 3dd4 a7a0 488a 34ae  .5.u}...=...H.4.
00000030: 66f5 b6d1 e139 3b82 d5a1 1941 4d02 b0b6  f....9;....AM...
00000040: d1c8 d8d0 fd3d ed31 c35c 2479 c6b6 2f07  .....=.1.\$y../.
00000050: 8ab5 0809 0f40 4c9e 6757 0e23 adae 7591  .....@L.gW.#..u.
00000060: 1a66 3d23 3d60 1be6 ad53 83eb 88ee cdba  .f=#=`...S......
00000070: 793f c65b aabf 5af9 8191 4100 efee 4c2c  y?.[..Z...A...L,
00000080: c07c 9e2f 8c7d 4bc5 744b 1e64 8869 9913  .|./.}K.tK.d.i..
00000090: 2693 6d76 0957 9bf5 5ef7 0d14 5e28 f319  &.mv.W..^...^(..
000000a0: 922d a614 5d69 9e0f 4a42 8606 e376 033e  .-..]i..JB...v.>
000000b0: c0c6 8c85 4505 a047 30a1 d7e7 ee6b 6f7a  ....E..G0....koz
000000c0: dbc7 951e 5720 a227 fd99 c0f6 fb52 95ec  ....W .'.....R..
000000d0: a60b c36f 1eea acaf e2dd c7a4 ec25 fbd1  ...o.........%..
000000e0: f505 8033 b099 1956 693f f5b4 2eca 32d5  ...3...Vi?....2.
000000f0: 8cb7 dc71 e54a 8912 3bf4 c667 dc54 35d6  ...q.J..;..g.T5.
```

```bash
echo "dOBQEtYlozOcFweWVnH1tz0ju295tVXP0E6/tvlWN6jtNR51fQjO7D3Up6BIijSuZvW20eE5O4LVoRlBTQKwttHI2ND9Pe0xw1wkeca2LweKtQgJD0BMnmdXDiOtrnWRGmY9Iz1gG+atU4PriO7Nunk/xluqv1r5gZFBAO/uTCzAfJ4vjH1LxXRLHmSIaZkTJpNtdglXm/Ve9w0UXijzGZItphRdaZ4PSkKGBuN2Az7AxoyFRQWgRzCh1+fua29628eVHlcgoif9mcD2+1KV7KYLw28e6qyv4t3HpOwl+9H1BYAzsJkZVmk/9bQuyjLVjLfcceVKiRI79MZn3FQ11g==" | base64 -d | wc -c

256
```

Let's open the link `https://ugupugu.roboepics.com`

```bash
$ curl https://ugupugu.roboepics.com/

UGUPUGU(1)

NAME
	Ugupugu - a service for encryption/decryption

DESCRIPTION
	Using this service, u can encrypt and decrypt any plain text using the most 
	special Pub/Priv rsa key ever existed.
	PKCS and OAEP seem stupid and unnecessary; REAL RSA has been implemented.
	Do NOT try to decrypt ur flag with this. its not permitted.

ROUTES
	*) GET /help
		This help
	*) GET /pubkey
		returns Pub key.
	*) POST /encrypt
		put ur plain text in body of POST.
	*) POST /decrypt
		put ur cipher text in body of POST.

EXAMPLES
	*) curl -X GET ugupugu.roboepics.com/pubkey 
	*) curl -X POST ugupugu.roboepics.com/encrypt -d "a s3cret text placed here"
	*) curl -X POST ugupugu.roboepics.com/decrypt -d <UR CIPHER>

BUGS
	Ofc there is no bug.

SEE ALSO
	rsa, rsa-padding, PKCS1, OAEP, openssl

AUTHORS:
	A former developer in Roboepics who has been fired.
```

We see a description about using this API for encryption and decryption:

## get public key
Let get the public key first:
```bash
curl https://ugupugu.roboepics.com/pubkey                                                            ✔  2m 21s   2.7.2  
E: 65537
N: 18715011074845201888461791635367939553127268741525950569055646875583327021443659607353245335187865361831529174071669661800528518176785167923308382984980321847478987926576247803348565556467000769050253772844145294990007795239704368742758715638684197107821145503822208902630562212196150687206173690351749551186916854004800008749003363909832293560576767718140701898004524379681439118806637039874040392205378664659395484677831078036091366325220167320887257243286797974984343134558810336555940238652681956118161528469286073332846230059435703156764997667143302728650989754913668998360685694621902578380578148606411339422571
```


## sample encryption
lets encrypt a message with decimal value of `0`

```py
	def encrypt(m):
		url = "https://ugupugu.roboepics.com/encrypt"

		resp = requests.post(url, data=m)
		data = resp.content
		return b64decode(data)

c2 = bytes_to_long(encrypt("\x00"))
print(c2)
```

```py
python3.10 test.py
0
```

As we see the outout is 0
```
m**e % n
0 ** e % n = 0
```

Let's try with value `1`
```py
```py
	def encrypt(m):
		url = "https://ugupugu.roboepics.com/encrypt"

		resp = requests.post(url, data=m)
		data = resp.content
		return b64decode(data)

c2 = bytes_to_long(encrypt("\x00"))
print(c2)
```

```py
python3.10 test.py
1
```

As we see the outout is 1
```
m**e % n
1 ** e % n = 1
```

**it's showing us there is no padding and it raw textbook RSA**

## sample decrytion

If we try to decrypt the encrypted output message we get this output which rejects from decrypting the flag

```bash
curl -X POST https://ugupugu.roboepics.com/decrypt -d "dOBQEtYlozOcFweWVnH1tz0ju295tVXP0E6/tvlWN6jtNR51fQjO7D3Up6BIijSuZvW20eE5O4LVoRlBTQKwttHI2ND9Pe0xw1wkeca2LweKtQgJD0BMnmdXDiOtrnWRGmY9Iz1gG+atU4PriO7Nunk/xluqv1r5gZFBAO/uTCzAfJ4vjH1LxXRLHmSIaZkTJpNtdglXm/Ve9w0UXijzGZItphRdaZ4PSkKGBuN2Az7AxoyFRQWgRzCh1+fua29628eVHlcgoif9mcD2+1KV7KYLw28e6qyv4t3HpOwl+9H1BYAzsJkZVmk/9bQuyjLVjLfcceVKiRI79MZn3FQ11g=="

Ugupugu rejects decrypting flags
```

# Solution
We can encrypt any message we want and also we can decrypt as well except for the encrypted flag\
RSA has a significant mathematical property named [Homomorphic](https://en.wikipedia.org/wiki/Homomorphism)\
In case of RSA textbook without any padding we can abuse this property property. To be brief it says
```
E(m1) = c1
E(m2) = c2
E(m1.m2) = c1.c2

(m1 ** e) % n = c1
(m2 ** e) % n = c2
((m1.m2) ** e) % n = c1.c2
```

Here is the scenario we will use according to this [link](https://crypto.stackexchange.com/questions/2323/how-does-a-chosen-plaintext-attack-on-rsa-work)
0. We have `c1` which is encrypted flag and we want to compute `m1` which is flag
1. We will encrypt a `\x02` message with decimal value of `2` and get `c2`
2. multiply `c1` with `c2` modulus `n` and get `c1.c2 % n`
3. decrypt `c1.c2` and get `m1.m2`
4. divide `m1.m2` by `m2` which is `2` and get `m1` which is the flag

Here is the final code

```py
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
print(long_to_bytes(flag).decode())
```

After running the code we get the encrypted message and the flag:
```
python3.10 solve.py
Ugupugu:
u are here and that means u are more fly than 99% of the population of the earth. :D
Welcome to RoboEpics Cyber Nobility. Here is ur flag:

--x xeroctf{ugupugu?use_padd1ng-for-rsa!} x--

P.S: Be kind to one another. ^~^
```

Here is the flag:
```
xeroctf{ugupugu?use_padd1ng-for-rsa!}
```

[solution code](https://github.com/KooroshRZ/CTF-Writeups/blob/main/XeroCTF2022-Teaser/rsa/solve.py)
<br>
> KouroshRZ for **AbyssalCruelty**