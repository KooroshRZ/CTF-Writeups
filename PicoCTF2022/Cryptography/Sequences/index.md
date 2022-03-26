# Sequences
Here is the chalenge code and description
```
Description

I wrote this linear recurrence function, can you figure out how to make it run fast enough and get the flag?Download the code here https://artifacts.picoctf.net/c/507/sequences.py. Note that even an efficient solution might take several seconds to run. If your solution is taking several minutes, then you may need to reconsider your approach.
```

The code
```py
import math
import hashlib
import sys
from tqdm import tqdm
import functools

ITERS = int(2e7)
VERIF_KEY = "96cc5f3b460732b442814fd33cf8537c"
ENCRYPTED_FLAG = bytes.fromhex("42cbbce1487b443de1acf4834baed794f4bbd0dfe2d6046e248ff7962b")

# This will overflow the stack, it will need to be significantly optimized in order to get the answer :)
@functools.cache
def m_func(i):
    if i == 0: return 1
    if i == 1: return 2
    if i == 2: return 3
    if i == 3: return 4

    return 55692*m_func(i-4) - 9549*m_func(i-3) + 301*m_func(i-2) + 21*m_func(i-1)


# Decrypt the flag
def decrypt_flag(sol):
    sol = sol % (10**10000)
    sol = str(sol)
    sol_md5 = hashlib.md5(sol.encode()).hexdigest()

    if sol_md5 != VERIF_KEY:
        print("Incorrect solution")
        sys.exit(1)

    key = hashlib.sha256(sol.encode()).digest()
    flag = bytearray([char ^ key[i] for i, char in enumerate(ENCRYPTED_FLAG)]).decode()

    print(flag)

if __name__ == "__main__":
    sol = m_func(ITERS)
    decrypt_flag(sol)
```

# Code Analysis
As we see there is a recursive function that for every step it uses its 4 previous steps.\
And from the comment, it will overflow the stack because the input 20000000 is too large.
```
# This will overflow the stack, it will need to be significantly optimized in order to get the answer :)
```
```py
~/CTF/picoctf2022/Crypto/Sequences  python3.9 sequences.py
Traceback (most recent call last):
  File "/home/kourosh/CTF/picoctf2022/Crypto/Sequences/sequences.py", line 38, in <module>
    sol = m_func(ITERS)
  File "/home/kourosh/CTF/picoctf2022/Crypto/Sequences/sequences.py", line 19, in m_func
    return 55692*m_func(i-4) - 9549*m_func(i-3) + 301*m_func(i-2) + 21*m_func(i-1)
  File "/home/kourosh/CTF/picoctf2022/Crypto/Sequences/sequences.py", line 19, in m_func
    return 55692*m_func(i-4) - 9549*m_func(i-3) + 301*m_func(i-2) + 21*m_func(i-1)
  File "/home/kourosh/CTF/picoctf2022/Crypto/Sequences/sequences.py", line 19, in m_func
    return 55692*m_func(i-4) - 9549*m_func(i-3) + 301*m_func(i-2) + 21*m_func(i-1)
  [Previous line repeated 496 more times]
RecursionError: maximum recursion depth exceeded
```

So we need to optimize the recursive function to find the `m_func(20000000)`.

# Failed solution tries
The first approach I chose to optimize the function was dynamic programming\
According to [this link](https://www.educative.io/courses/grokking-dynamic-programming-patterns-for-coding-interviews/m2G1pAq0OO0), There are two methods to implement it.
## Top-down with Memoization
This method is used for optimizing recursive functions to avoid duplicate functions calls.\
In this approach, we try to solve the bigger problem by recursively finding the solution to smaller sub-problems. Whenever we solve a sub-problem, we cache its result so that we don’t end up solving it repeatedly if it’s called multiple times. Instead, we can just return the saved result. This technique of storing the results of already solved subproblems is called **Memoization**.[1](https://www.educative.io/courses/grokking-dynamic-programming-patterns-for-coding-interviews/m2G1pAq0OO0#Top-down-with-Memoization)
<br>
But just storing values and starting from `20000000` won't e enough because before reaching `m_func(0), m_func(1), m_func(2), m_func(3)` the stack will overflow and exit the program.\
So I started from m_func(4) and increasing i inside m_func(i) for each level and store the returned value f(4)=x, f(5)=y, .... But because of massive increments in return values for higher inputs 100,1000,... the amount of RAM to handle this memoization program will be huge and we’re not capable of doing that(I also tried storing values on the hard drive and starting the program again but it was too slow)

<br>
Here is the example code is used for memoization but it failed because of slow speed and a large amount of ram it needed for storing values(storing on hard disk also didn’t work because of low speed on higher values)
```py
import functools

ITERS = int(2e7)
VERIF_KEY = "96cc5f3b460732b442814fd33cf8537c"
ENCRYPTED_FLAG = bytes.fromhex("42cbbce1487b443de1acf4834baed794f4bbd0dfe2d6046e248ff7962b")

values = {
    "0": 1,
    "1": 2,
    "2": 3,
    "3": 4
}

@functools.cache
def m_func(i):
    i = int(i)
    if str(i) in values:
        return values[str(i)]
    return 55692*m_func(i-4) - 9549*m_func(i-3) + 301*m_func(i-2) + 21*m_func(i-1)

# ITERS = 20000000
for i in range(4, 5):
    result = m_func(str(i))
    values[str(i)] = result

prin
for k in values:
    print(values)
```

## Bottom-up with Tabulation
Tabulation is the opposite of the top-down approach and avoids recursion. In this approach, we solve the problem “bottom-up” (i.e. by solving all the related sub-problems first). This is typically done by filling up an n-dimensional table. Based on the results in the table, the solution to the top/original problem is then computed.[2](https://www.educative.io/courses/grokking-dynamic-programming-patterns-for-coding-interviews/m2G1pAq0OO0#Bottom-up-with-Tabulation)
<br>
I also tried Tabulation which starts from 0 and solves and calculates lower values without recursively calling the function and going upwards. This method solved the RAM problem but it was also very slow which I ran it for about 48 hours and it didn’t reach 20000000 which is our needed value so this method failed too.

Here is the example code I used for Tabulation.
This method will reach the solution and also it fixed RAM and stack problem, but it will take too long.
```py
import functools
from collections import deque

ITERS = int(2e7)
VERIF_KEY = "96cc5f3b460732b442814fd33cf8537c"
ENCRYPTED_FLAG = bytes.fromhex("42cbbce1487b443de1acf4834baed794f4bbd0dfe2d6046e248ff7962b")

values = deque([1,2,3,4])

@functools.cache
def m_func(i):

    for _ in range(4, i+1):
        values[0] = 55692*values[0] - 9549*values[1] + 301*values[2] + 21*values[3]
        values.rotate(-1)

    print(values[3])

# ITERS = 20000000
result = m_func(ITERS)
```



# Main and Optimum Solution
After a couple of days of failing, I heard from a friend that there are ways to solve recursive functions by generating functions of sequences. I searched and studied a lot about them and found some useful resources.
<br>
[Generating functions](https://en.wikipedia.org/wiki/Generating_function): In [mathematics](https://en.wikipedia.org/wiki/Mathematics "Mathematics"), a **generating function** is a way of encoding an [infinite sequence](https://en.wikipedia.org/wiki/Infinite_sequence "Infinite sequence") of numbers (`an`) by treating them as the [coefficients](https://en.wikipedia.org/wiki/Coefficient "Coefficient") of a [formal power series](https://en.wikipedia.org/wiki/Formal_power_series "Formal power series"). This series is called the generating function of the sequence.
By generating functions we can calculate the coefficient of a specific element of sequence `an` which is actually `f(n)`.
Actually we have linear recurrence function and after further studies I realized that we can also solve these functions with generating functions and find `f(20000000)` which is what we want
<br>
I used the wolfram engine for Linux to find the generating function of this recurrence equation.
Here is the generating function of our linear recurrence function:
```bash
kourosh@irvm-69871:~/ctf/1$ wolframscript 
Wolfram Language 13.0.1 Engine for Linux x86 (64-bit)
Copyright 1988-2022 Wolfram Research, Inc.

In[1]:= FindGeneratingFunction[{1,2,3,4,37581,873142,29776743,529489144,13837399761,214250532682,5266553049483}, x]                                   

                              2         3
             -1 + 19 x + 340 x  - 8888 x
Out[1]= ---------------------------------------
                         2         3          4
        -1 + 21 x + 301 x  - 9549 x  + 55692 x

```

And here is the commands I used for specific sequence(for example n=12 which is actually `m_func(12)`)
```bash
In[3]:= SeriesCoefficient[%, 12]

Out[3]= 1831268671595541

In[4]:=                                                                                                                                              
```

We can also use this command for example `m_func(20)` which is 20's coefficient of the sequences
```bash
In[4]:= SeriesCoefficient[(-1 + 19*x + 340*x^2   - 8888*x^3)/(-1 + 21*x + 301*x^2 - 9549*x^3 + 55692*x^4), {x, 0, 20}]

Out[4]= 23654235486457205901623901
```

Ok we found a way to automate the direct calculation of the coefficient of sequences.\
Now we need to find the 20000000 sequences from the above generating function with this command
```bash
In[4]:= SeriesCoefficient[(-1 + 19*x + 340*x^2   - 8888*x^3)/(-1 + 21*x + 301*x^2 - 9549*x^3 + 55692*x^4), {x, 0, 20000000}]
```
But this also needs a lot of RAM space and it failed again\
So I continued my studies again and I found a solution to directly extract the function which calculates the `nth` sequence of the linear recurrence function (`an`)\
This function will produce the nth sequence directly without looping. for example:
```
T(n) = 2*T(n-1) + 1
The direct function of n will be
f(n) = 2**n - 1 (Easy Huh?! But how to extract this function)
```

To solve these linear recurrence functions you can study this [PDF](https://www.math.cmu.edu/~af1p/Teaching/Combinatorics/Slides/Generating-Functions.pdf)\
But fortunately, wolfram has automated linear recurrence function solving platform which will extract this function [automatically](https://www.wolframalpha.com/input?i=f%28n%29%3D55692*f%28n-4%29+-+9549*f%28n-3%29+++301*f%28n-2%29+++21*f%28n-1%29%2C+f%281%29%3D1%2C+f%282%29%3D2%2C+f%283%29%3D3%2C+f%284%29%3D4)\
And here is the direct solution to our linear recurrence function:
```
         (-20956*(-21)**n) + 2792335*2**(2*n + 3)*(3**n) - (22739409*13**n) + (2279277*17**n)
f(n) =	______________________________________________________________________________________
									              11639628
```

And here is the refined function with a direct solution:
```py
import hashlib
import sys

ITERS = int(2e7)
VERIF_KEY = "96cc5f3b460732b442814fd33cf8537c"
ENCRYPTED_FLAG = bytes.fromhex("42cbbce1487b443de1acf4834baed794f4bbd0dfe2d6046e248ff7962b")


def decrypt_flag(sol):
    sol = sol % (10**10000)
    sol = str(sol)
    sol_md5 = hashlib.md5(sol.encode()).hexdigest()

    if sol_md5 != VERIF_KEY:
        print("Incorrect solution")
        sys.exit(1)

    key = hashlib.sha256(sol.encode()).digest()
    flag = bytearray([char ^ key[i] for i, char in enumerate(ENCRYPTED_FLAG)]).decode()

    print(flag)


def n_seq(n):
    result = ((-20956*(-21)**n) + 2792335*2**(2*n + 3)*(3**n) - (22739409*13**n) + (2279277*17**n))//11639628
    return result

sol = n_seq(ITERS+1)
decrypt_flag(sol)
```

After running the code and waiting for a bit (because of big number calculations) we found the correct solution and decrypted the flag. yay!
```bash
kourosh@irvm-69871:~/ctf/1$ python3.9 solve.py
picoCTF{b1g_numb3rs_689693c6}
```

And here is the flag:
```
picoCTF{b1g_numb3rs_689693c6}
```

[solution code](https://github.com/KooroshRZ/CTF-Writeups/blob/main/PicoCTF2022/Cryptography/Sequences/solve.py)
<br>
> KouroshRZ for **Evento**