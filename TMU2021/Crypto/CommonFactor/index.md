# Common Factor
Here is the challenge code and Description
```
How much do you know about the RSA algorithm?
```

```python
from Crypto.Util.number import *

from functools import reduce

def encrypt(msg, n):
	enc = pow(bytes_to_long(msg), e, n)
	return enc

e = 65537

primes = [getPrime(2048) for i in range(5)]
n = reduce(lambda a, x: a * x, primes, 1)
print(n)

x1 = primes[1] ** 2
x2 = primes[2] ** 2
x3 = primes[1] * primes[2]
y1 = x1 * primes[2] + x2 * primes[1]
y2 = x2 * (primes[3] + 1) - 1
y3 = x3 * (primes[3] + 1) - 1
print(x2 + x3 + y1)
print(y2 + y3)

with open('flag', 'rb') as f:
	flag = f.read()
	print(encrypt(flag, n))
```

# Solution

We have equations like this
```python
n  = primes[0] * primes[1] * primes[2] * primes[3] * primes[4]
v1 = x2 + x3 + y1
v2 = y2 + y3

v1 = primes[2]**2 + primes[1]*primes[2] + (primes[1]**2)*primes[2] + primes[1]*(primes[2]**2)
v2 = (primes[2]**2)*primes[3] + primes[2]**2 + primes[1]*primes[2]*primes[3] + primes[1]*primes[2] - 2
```

We know that `n` and `v1` both are divisible by `primes[2]` so we can calculate Greatest Common Factor of `n` and `v1` `gcd(v1,n)` to find `primes[2]`
```python
# p2
p2 = gcd(n, v1)
if n % p2 == 0: # confirm for correct p2 value
	print(p2)
```

Then by having `primes[2]` and `v1` we can calculate `p1` with 2 degree equations solves
```
# p1
a1 = p2
b1 = p2**2 + p2
c1 = p2**2 - value1
delta1 = b1**2 - 4*a1*c1

p1 = (-b1 + nth_root(delta1, 2)) // (2*a1)
if n % p1 == 0: # confirm for correct p2 value
	print(p1)
```

By having `primes[1]` and `primes[2]` we also can find `primes[3]` through v2 linear equations
```python
# p3
p3 = (value2 - (p2**2 + p1*p2) + 2) // (p1*p2 + p2**2)
if n % p3 == 0: # confirm for correct p3 value
	print(p3)
```


OK, we have 3 factors of our 5 factor n, But to decrypt the flag that's enough and no need for other factors [link](https://crypto.stackexchange.com/questions/44110/rsa-with-3-primes)
```python
phi1 = (p1-1)*(p2-1)
d1 = inverse(e, phi1)
flag = pow(enc % p1, d1, p1)
print(long_to_bytes(flag))
```

and here is the flag
```
flag: b'TMUCTF{Y35!!!__M4Y_N0t_4lW4y5_N33d_4ll_p21M3_f4c70R5}'
```

[solution code](https://github.com/KooroshRZ/CTF-Writeups/blob/main/TMU2021/Crypto/CommonFactor/solve.py)