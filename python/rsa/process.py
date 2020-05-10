import random

def primelt(n):
    return list(filter(isprime, range(2, n)))

allPrimeLt10000 = primelt(10000)

def isprime(n):
    for i in range(2, int(n/2) + 1):
        if n % i == 0:
            return False
    return True

def oulan(p, q):
    return (p - 1) * (q - 1)

def n():
    return oulan(random.choice(allPrimeLt10000), random.choice(allPrimeLt10000))

doc = '''
c === m ** e mod n
m === c ** d mod n

c, m could be cipher or plain
(e, n), (d, n) could be public key or private key

e and d should satified:

    (e * d) mod \epsilon(n) == 1

    p * q = n

    \epsilon(n) = \epsilon(p) * \epsilon(q) = (p - 1) * (q - 1)


'''
