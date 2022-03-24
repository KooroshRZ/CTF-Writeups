# Very Smooth

Here is the challenge code and Description.

## Description
```
Forget safe primes... Here, we like to live life dangerously... >:)
```

## Challenge code and Output

```py
#!/usr/bin/python

from binascii import hexlify
from gmpy2 import *
import math
import os
import sys

if sys.version_info < (3, 9):
    math.gcd = gcd
    math.lcm = lcm

_DEBUG = False

FLAG  = open('flag.txt').read().strip()
FLAG  = mpz(hexlify(FLAG.encode()), 16)
SEED  = mpz(hexlify(os.urandom(32)).decode(), 16)
STATE = random_state(SEED)

def get_prime(state, bits):
    return next_prime(mpz_urandomb(state, bits) | (1 << (bits - 1)))

def get_smooth_prime(state, bits, smoothness=16):
    p = mpz(2)
    p_factors = [p]
    while p.bit_length() < bits - 2 * smoothness:
        factor = get_prime(state, smoothness)
        p_factors.append(factor)
        p *= factor

    bitcnt = (bits - p.bit_length()) // 2

    while True:
        prime1 = get_prime(state, bitcnt)
        prime2 = get_prime(state, bitcnt)
        tmpp = p * prime1 * prime2
        if tmpp.bit_length() < bits:
            bitcnt += 1
            continue
        if tmpp.bit_length() > bits:
            bitcnt -= 1
            continue
        if is_prime(tmpp + 1):
            p_factors.append(prime1)
            p_factors.append(prime2)
            p = tmpp + 1
            break

    p_factors.sort()

    return (p, p_factors)

e = 0x10001

while True:
    p, p_factors = get_smooth_prime(STATE, 1024, 16)
    if len(p_factors) != len(set(p_factors)):
        continue
    # Smoothness should be different or some might encounter issues.
    q, q_factors = get_smooth_prime(STATE, 1024, 17)
    if len(q_factors) != len(set(q_factors)):
        continue
    factors = p_factors + q_factors
    if e not in factors:
        break

if _DEBUG:
    import sys
    sys.stderr.write(f'p = {p.digits(16)}\n\n')
    sys.stderr.write(f'p_factors = [\n')
    for factor in p_factors:
        sys.stderr.write(f'    {factor.digits(16)},\n')
    sys.stderr.write(f']\n\n')

    sys.stderr.write(f'q = {q.digits(16)}\n\n')
    sys.stderr.write(f'q_factors = [\n')
    for factor in q_factors:
        sys.stderr.write(f'    {factor.digits(16)},\n')
    sys.stderr.write(f']\n\n')

n = p * q

m = math.lcm(p - 1, q - 1)
d = pow(e, -1, m)

c = pow(FLAG, e, n)

print(f'n = {n.digits(16)}')
print(f'c = {c.digits(16)}')
```

```
n = c5261293c8f9c420bc5291ac0c14e103944b6621bb2595089f1641d85c4dae589f101e0962fe2b25fcf4186fb259cbd88154b75f327d990a76351a03ac0185af4e1a127b708348db59cd4625b40d4e161d17b8ead6944148e9582985bbc6a7eaf9916cb138706ce293232378ebd8f95c3f4db6c8a77a597974848d695d774efae5bd3b32c64c72bcf19d3b181c2046e194212696ec41f0671314f506c27a2ecfd48313e371b0ae731026d6951f6e39dc6592ebd1e60b845253f8cd6b0497f0139e8a16d9e5c446e4a33811f3e8a918c6cd917ca83408b323ce299d1ea9f7e7e1408e724679725688c92ca96b84b0c94ce717a54c470d035764bc0b92f404f1f5
c = 1f511af6dd19a480eb16415a54c122d7485de4d933e0aeee6e9b5598a8e338c2b29583aee80c241116bc949980e1310649216c4afa97c212fb3eba87d2b3a428c4cc145136eff7b902c508cb871dcd326332d75b6176a5a551840ba3c76cf4ad6e3fdbba0d031159ef60b59a1c6f4d87d90623e5fe140b9f56a2ebc4c87ee7b708f188742732ff2c09b175f4703960f2c29abccf428b3326d0bd3d737343e699a788398e1a623a8bd13828ef5483c82e19f31dca2a7effe5b1f8dc8a81a5ce873a082016b1f510f712ae2fa58ecdd49ab3a489c8a86e2bb088a85262d791af313b0383a56f14ddbb85cb89fb31f863923377771d3e73788560c9ced7b188ba97
```

# Code Analysis

First of all let's analyze the challenge code\
This section will produce two factors `(p,q)` for key generation.

```py
while True:
    p, p_factors = get_smooth_prime(STATE, 1024, 16)
    if len(p_factors) != len(set(p_factors)):
        continue
    # Smoothness should be different or some might encounter issues.
    q, q_factors = get_smooth_prime(STATE, 1024, 17)
    if len(q_factors) != len(set(q_factors)):
        continue
    factors = p_factors + q_factors
    if e not in factors:
        break
```

These 2 functions will generate a prime number with these conditions:
1. The `get_smooth_prime(STATE, 1024, 16)` function will generate a 16bit-smooth number
2. Acording to this [link](https://en.wikipedia.org/wiki/Smooth_number), an `n-smooth` number is an integer whose prime factors are all less than or equal to n.
3. Regarding above definition, the output of `get_smooth_prime` will be a prime number which `p-1` is an `65536-smooth` number. that means all prime factors of the `p-1` will be less than `65536` and there is also no duplicate of any prime factors.
4. The `get_smooth_prime(STATE, 1024, 17)` will be called again for second prime factor(q) which `q-1` is a `17bit-smooth` number `(131072-smooth)`

```py
def get_prime(state, bits):
    return next_prime(mpz_urandomb(state, bits) | (1 << (bits - 1)))

def get_smooth_prime(state, bits, smoothness=16):
    p = mpz(2)
    p_factors = [p]
    while p.bit_length() < bits - 2 * smoothness:
        factor = get_prime(state, smoothness)
        p_factors.append(factor)
        p *= factor

    bitcnt = (bits - p.bit_length()) // 2

    while True:
        prime1 = get_prime(state, bitcnt)
        prime2 = get_prime(state, bitcnt)
        tmpp = p * prime1 * prime2
        if tmpp.bit_length() < bits:
            bitcnt += 1
            continue
        if tmpp.bit_length() > bits:
            bitcnt -= 1
            continue
        if is_prime(tmpp + 1):
            p_factors.append(prime1)
            p_factors.append(prime2)
            p = tmpp + 1
            break

    p_factors.sort()
```

After investigating overall code, it will generate primes `p,q` which `p-1` and `q-1` are both `16bit and 17bit smooth` numbers which means all of `p-1` factors are less than `2**16` or `65536` and all of `q-1` factors are less than `2**17` or `131072`.

Here is the hint picoCTF offered:
```
Don't look at me... Go ask Mr. Pollard if you need a hint!
```

So Let's search `pollard` and `smooth number` keywords

# Solution

We wanna factor `n` and recover `p,q` then `d` and decrypt the ciphertext `c`\
After searching about `pollard` and `smooth number` keywords, I found [Pollard's p−1] algorithm(https://en.wikipedia.org/wiki/Pollard%27s_p_%E2%88%92_1_algorithm)\
As we see, it's an integer factorization algorithm which can be applied for those numbers whose prime factors(`p-1`) are `powersmooth`\
By definition 
```
Further, m is called B-powersmooth (or B-ultrafriable) if all prime powers p**v dividing m satisfy:

p**v <= B
```

Here we can use `Pollard's p − 1` algorithm, because our integer `n`'s factor `p` is `65536-powersmooth` and factor `q` is `131072-powersmooth` which satisfy our conditions.

## Pollard's p − 1 Algorithm

Here is the overall steps:

1. select a smoothness bound `B` (we should use 65535)
2. choose a random base `a` coprime to `n`
3. define `M = factorial(B)`
4. compute `g = gcd(a**M - 1, n)`
5. if `1 < g < n` then `g` is one of the factors
6. if `g == 1` select larger `B` and try again
7. if `g == n` select smaller `B` and try again

## Pollard's p − 1 Algorithm's proof
Let's see how this algorithm works

### Fermat's Little Theorem

We know that for every prime number `p` and a random number `a` coprime to `p` we can write
```
a**(p-1) % p = 1
or
a**(p-1) -1 = p*r
```
In other words `a**(p-1) - 1` has two factors `p,r` and `p` is prime\
We can also multiply `p-1` with `k`:
```
a**[k*(p-1)] % p = 1
or
a**[k*(p-1)] -1 = p*s
```

### The proof
From previous equations we can conclude:
```
gcd(a**[k*(p-1)]-1 = p*s, n) = p
B = k*(p-1)
gcd((a**B)-1, n) = p
```

If we can calculate `B` and choose any integer `a` co-prime to `n`(2 is best choice), then we can find `p` with `gcd` operation. simple huh?! But how to find `B`\
We know that:
```
B = k*(p-1)
p-1 = p1 * p2 * p3 ... * px
```
And we know that `p-1` is `powesmooth` which means that all factors of `p-1`(`p1, p2, ..., px`) is less than `65536`
So if we choose `B=1*2*3*4*...*65535` and calculate that we can assure that `B` has `p` inside its factor and gcd of `a**B - 1` with `n` will result in `p` which is one of the factors. Sounds cool!


## solve code
After proving the algorithm, let's code all these steps to find `p,q` and recover private key `d` and decrypt the flag:
```py
from gmpy2 import fac
from math import gcd
from Crypto.Util.number import *
from sympy import true

n = 0xc5261293c8f9c420bc5291ac0c14e103944b6621bb2595089f1641d85c4dae589f101e0962fe2b25fcf4186fb259cbd88154b75f327d990a76351a03ac0185af4e1a127b708348db59cd4625b40d4e161d17b8ead6944148e9582985bbc6a7eaf9916cb138706ce293232378ebd8f95c3f4db6c8a77a597974848d695d774efae5bd3b32c64c72bcf19d3b181c2046e194212696ec41f0671314f506c27a2ecfd48313e371b0ae731026d6951f6e39dc6592ebd1e60b845253f8cd6b0497f0139e8a16d9e5c446e4a33811f3e8a918c6cd917ca83408b323ce299d1ea9f7e7e1408e724679725688c92ca96b84b0c94ce717a54c470d035764bc0b92f404f1f5
c = 0x1f511af6dd19a480eb16415a54c122d7485de4d933e0aeee6e9b5598a8e338c2b29583aee80c241116bc949980e1310649216c4afa97c212fb3eba87d2b3a428c4cc145136eff7b902c508cb871dcd326332d75b6176a5a551840ba3c76cf4ad6e3fdbba0d031159ef60b59a1c6f4d87d90623e5fe140b9f56a2ebc4c87ee7b708f188742732ff2c09b175f4703960f2c29abccf428b3326d0bd3d737343e699a788398e1a623a8bd13828ef5483c82e19f31dca2a7effe5b1f8dc8a81a5ce873a082016b1f510f712ae2fa58ecdd49ab3a489c8a86e2bb088a85262d791af313b0383a56f14ddbb85cb89fb31f863923377771d3e73788560c9ced7b188ba97

a = 2
B = 65535

while True:

	b = fac(B)

	tmp1 = n
	tmp2 = pow(a, b, n) - 1
	gcd_value = gcd(tmp1, tmp2)

	if gcd_value == 1:
		B += 1
	elif gcd_value == n:
		B -= 1
	else:
		print(f"[+] p factor : {gcd_value}")

		p = gcd_value
		q = n // p
		e = 0x10001

		print(f"[+] q factor : {q}")

		phi = (p-1)*(q-1)
		d = inverse(e, phi)

		m = pow(c, d, n)

		flag = long_to_bytes(m)

		print(flag)

		break

```

After running above code we recovered `p,q` and decrypted the flag:
```bash
~/CTF/picoctf2022/Crypto/VerySmooth  python3.9 solve.py
[+] p factor : 159652342260602436611264882107764540496206777532515381978886917602247902747922672308128228056532167311635408138845484288179466203049041882723045592330122232567342518194630068422135188545880928509542459095514667379085548962076958641693004621121073173222707331672786582779407036356311260724097659870075337003627
[+] q factor : 155886972960664534013041814351782927840465950022742711153704061512767231252254923859358385447688708709761645561788434482490726299524712681978677060822069411804436435368518028882769406676617745559724738774782701625211779174370759988895228070938831967483401953816901269670197361506466713077188578114638897325343
b'picoCTF{7c8625a1}'
```
Here is the flag
```
picoCTF{7c8625a1}
```

[solution code](https://github.com/KooroshRZ/CTF-Writeups/blob/main/PicoCTF2022/Crypto/VerySmooth/solve.py)
<br>
> KouroshRZ for **Evento**
