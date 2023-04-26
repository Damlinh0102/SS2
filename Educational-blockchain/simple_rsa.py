"""
Created on Mon Mar 13 10:01:56 2023
Based on the theory from this page:
    https://sahandsaba.com/cryptography-rsa-part-1.html
And some code from this source:
    https://gist.github.com/djego/97db0d1bc3d16a9dcb9bab0930d277ff
With some optimizations:
    - choosing the e value
    - using the built-in pow function for calculation large exponentials
@author: Quan
"""

import random
from math import gcd
import base64


def byte_length(n):
    return (n.bit_length() + 7) // 8


def is_prime(num):  # fast
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num ** 0.5) + 2, 2):
        if num % n == 0:
            return False
    return True


def find_two_primes():
    a = random.randint(2000, 9999)
    while not is_prime(a):
        a += 1
    check = True
    while check:
        b = random.randint(2000, 9999)
        while (not is_prime(b)):
            b += 1
        if b != a:
            check = False
    return (a, b)


def genkey():
    p, q = find_two_primes()
    n = p * q
    m = (p - 1) * (q - 1)
    e = random.randint(200, 1999)  # small exponent
    while gcd(e, m) != 1:  # e & m are co-prime
        e = random.randint(200, 1999)
    d = pow(e, -1, m)
    return (e, n, d)


def padding(data, byte_len):
    # add padding to 'data' so that: len(data) % byte_len == 0
    # padding is done on the right of the bytes object
    # remainder = 0 -> no padding
    # remainder = 1 -> 3 - 1 = 2 bytes of padding
    # remainder = 2 -> 3 - 2 = 1 byte of padding
    remainder = len(data) % byte_len
    if (remainder != 0):
        data = data + bytes(byte_len - remainder)
    return data


def remove_padding(data, byte_len):
    # start at the last byte,
    # remove any '\x00' byte (which equals 0)
    index = len(data) - 1
    while (data[index] == 0):
        index -= 1
    return data[0: index + 1]


def encrypt(data, key):
    # k can be e for public key or d for private key
    [k, n] = key
    cipher = bytes()
    # determine block length
    keylen = byte_length(n)
    blocklen = keylen - 1
    data = padding(data, blocklen)
    for i in range(0, len(data), blocklen):
        block = data[i:i + blocklen]
        a = int.from_bytes(block)
        c = int(pow(a, k, n))
        cipher = cipher + c.to_bytes(keylen)
    return cipher


def decrypt(cipher, key):
    # k can be e for public key or d for private key
    [k, n] = key
    plain = bytes()
    keylen = byte_length(n)
    blocklen = keylen - 1
    for i in range(0, len(cipher), keylen):
        block = cipher[i: i + keylen]
        c = int.from_bytes(block)
        a = pow(c, k, n)
        plain = plain + a.to_bytes(blocklen)
    return remove_padding(plain, blocklen)


def encrypt_b64(bytes_data, key):
    # binary -> base64 string
    cipher = encrypt(bytes_data, key)
    return base64.b64encode(cipher).decode()


def decrypt_b64(b64cipher, key):
    # base64 string -> binary
    cipher = base64.b64decode(b64cipher)
    return decrypt(cipher, key)


def test():
    e, n, d = genkey()
    cipher = encrypt("Chaothichao".encode(), (e, n))
    b64 = base64.b64encode(cipher).decode()
    plain = decrypt(cipher, (d, n)).decode()

# (e, n): public key
# (d, n): private key

# e, d, n = (1267, 12966523, 30155681)

# str1 = '8KMgZffYjtzpeLq1cv6nLuwCaxeEG9c3jw6pVwFvemk='
# print(encrypt_str(str1, (d, n)))


# cipher = encrypt_str("Xin chào cả nhà", (d, n))
# print(cipher)
# plaintext = decrypt_str(cipher, (e, n))
# print(plaintext)
