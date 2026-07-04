"""
RSA Encryption
--------------
A from-scratch, educational implementation of RSA public-key encryption.

Steps implemented:
1. Generate two distinct random primes p and q (Miller-Rabin primality test).
2. Compute n = p * q  and  phi(n) = (p-1)(q-1).
3. Choose public exponent e such that gcd(e, phi) = 1 (commonly 65537).
4. Compute private exponent d = e^-1 mod phi (via the Extended Euclidean
   Algorithm).
5. Public key  = (e, n)   Private key = (d, n)
6. Encrypt each character's ordinal value: c = m^e mod n
7. Decrypt each ciphertext integer:        m = c^d mod n

NOTE: Prime sizes here are intentionally small (default 16 bits per prime)
so the demo runs instantly in a browser and stays readable. This is for
learning the algorithm, not for securing real data -- production RSA uses
primes that are 1024+ bits each.
"""

import random


def is_prime(n: int, rounds: int = 20) -> bool:
    """Miller-Rabin probabilistic primality test."""
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    for p in small_primes:
        if n % p == 0:
            return n == p

    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(rounds):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bits: int) -> int:
    """Generate a random prime number with the given bit length."""
    while True:
        candidate = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_prime(candidate):
            return candidate


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a: int, b: int):
    """Returns (g, x, y) such that a*x + b*y = g = gcd(a, b)."""
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y


def mod_inverse(a: int, m: int) -> int:
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    return x % m


def generate_keypair(bits: int = 16):
    """Generate an RSA keypair. Returns a dict with public/private keys."""
    p = generate_prime(bits)
    q = generate_prime(bits)
    while q == p:
        q = generate_prime(bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    if e >= phi or gcd(e, phi) != 1:
        e = 3
        while gcd(e, phi) != 1:
            e += 2

    d = mod_inverse(e, phi)

    return {
        "p": p,
        "q": q,
        "n": n,
        "phi": phi,
        "public": (e, n),
        "private": (d, n),
    }


def rsa_encrypt(message: str, public_key) -> list:
    """Encrypt a string message character-by-character. Returns a list of ints."""
    e, n = public_key
    if any(ord(ch) >= n for ch in message):
        raise ValueError(
            "Message contains a character too large for this key size. "
            "Generate a larger key or use shorter/simpler text."
        )
    return [pow(ord(ch), e, n) for ch in message]


def rsa_decrypt(cipher_values: list, private_key) -> str:
    """Decrypt a list of ints back into the original string message."""
    d, n = private_key
    return "".join(chr(pow(c, d, n)) for c in cipher_values)
