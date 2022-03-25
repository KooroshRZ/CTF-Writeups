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