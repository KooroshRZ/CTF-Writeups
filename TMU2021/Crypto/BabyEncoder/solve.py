from Crypto.Util.number import long_to_bytes

def displace(a, base):
    res = []
    for i in range(base):
        if base + i >= len(a):
            for j in range(base - 1, i - 1, -1):
                res.append(a[j])
            return res
        res.append(a[base + i])
        res.append(a[i])
    for j in range(len(a) - 1, 2 * base - 1, -1):
        res.append(a[j])
    return res


def reverse(lst):
    return [ele for ele in reversed(lst)]


def decode1(data):

    size = len(data)
    new = []

    for i in range(0, size, 3):
        a0 = (data[i] - data[i+1] + data[i+2]) // 2
        a1 = (data[i+1] - data[i+2] + data[i]) // 2
        a2 = (data[i+2] - data[i] + data[i+1]) // 2

        new.append(a0)
        new.append(a1)
        new.append(a2)
        
    return(new)

def decode2(data):

    size = len(data)
    for i in range(size-1, -1, -1):
        data[i] ^= data[size - i - 1]
 
    return(data)

def decode3(data):

    first = ord('}')
    size = len(data)
    new1 = []

    for i in range(size-1, -1, -1):

        first = first ^ data[i]
        new1.append(first)
    
    new1 = reverse(new1)
    new2 = []
    for i in range(size):
        new2.append(new1[(i+1)%size])

    return new2


test = [ord(f) for f in long_to_bytes(28946494946812141829547706026065914605092406854105997612241563383442514740934913838546119691331952671988567947306226900850151388621540356510466883510328793101483278519506803779932615196763052658252298923048223762802716830885754352726914690907223838594044069643833511017514637891042919056).decode()]

flags = True

for i in range(1, 30):
    test = displace(test, 72)
    
for i in range(1, 310):
    test = displace(test, 66)

for i in range(1, 4290):
    test = displace(test, 60)

for i in range(1, 2590):
    test = displace(test, 54)

for i in range(1, 37128):
    test = displace(test, 48)

for i in range(1, 168):
    test = displace(test, 42)

for i in range(1, 18):
    test = displace(test, 36)

for i in range(1, 60):
    test = displace(test, 30)

for i in range(1, 42):
    test = displace(test, 24)

for i in range(1, 36):
    test = displace(test, 18)

for i in range(1, 20):
    test = displace(test, 12)

for i in range(1, 12):
    test = displace(test, 6)

print(test)

size = len(test)

test1 = decode1(test)
print(test1)

test2 = decode2(test1)
print(test2)

test3 = decode3(test2)
print(test3)

flag = ''.join(chr(test3[i]) for i in range(size))
print(flag)