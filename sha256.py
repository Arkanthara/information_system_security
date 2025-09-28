from SHAConstants import *
import numpy as np

def join_table(table: list[chr] = ['t', 'e', 's', 't']) -> str:
    return ''.join(i for i in table)


def block2int(binary: str) -> np.array:
    binaries_list = [join_table(binary[i: i + 32]) for i in range(0, len(binary), 32)]
    uint32_list = [np.uint32(int(i, 2)) for i in binaries_list]
    return np.array(uint32_list)

def rotate(binary: int, shift: int, left: bool = False) -> int:
    shifted = np.array(list(format(binary, '032b')))
    assert shift <= len(shifted), "Shift must be <= number of bits !"
    if left:
        shifted = np.concatenate((shifted[shift:], shifted[:shift]))
    else:
        shifted = np.concatenate((shifted[-shift:], shifted[:-shift]))
    return np.uint32(int(join_table(shifted), 2))
    

def padding(msg: str = "coucou") -> str:
    tmp = [format(ord(i), '08b') for i in msg]
    binary = join_table(tmp)
    length = format(len(binary), '064b')
    binary += '1'
    current_length = len(length) + len(binary)
    K = 512 * (current_length // 512 + 1) - current_length
    binary += '0' * K + length
    return binary

def sha256(msg: str = "coucou") -> str:
    binary = padding(msg)
    binary = np.array(list(binary))
    binary = binary.reshape(-1, 512)
    if len(binary.shape) == 1:
        binary = np.array([binary])
    assert len(binary.shape) == 2, "Table of binary must be 2D !"
    R = list(IV)
    for i in range(len(binary)):
        R = one_way(binary[i], R)
    result = "".join(i for i in [hex(j) for j in R])
    return result
    
def one_way(binary: str, R):
    assert len(binary) == 512, f"Len of binary must be 512 ! actual {len(binary)} with shape {binary.shape}"
    W = list(block2int(binary))
    rotate(W[0], 3, True)
    for i in range(16, 64):
        s_0 = rotate(W[i - 15], 7) ^ rotate(W[i - 15], 18) ^ (W[i - 15] >> 3)    # Possibly change the value of 15 to 14 because python indexing...
        s_1 = rotate(W[i - 2], 17) ^ rotate(W[i - 2], 19) ^ (W[i - 2] >> 10)
        W.append(np.uint32((np.int64(W[i - 16]) + np.int64(s_0) + np.int64(W[i - 7]) + np.int64(s_1)) % 2**32))
    assert len(W) == 64, "Len of W must be 64 !"
    return compression(W, R)



def compression(W, R):
    a = R[0]
    b = R[1]
    c = R[2]
    d = R[3]
    e = R[4]
    f = R[5]
    g = R[6]
    h = R[7]
    for i in range(64):
        x_1 = rotate(e, 6) ^ rotate(e, 11) ^ rotate(e, 25)
        ch = (e & f) ^ ((~e) & g)
        x_2 = rotate(a, 2) ^ rotate(a, 13) ^ rotate(a, 22)
        maj = (a & b) ^ (a & c) ^ (b & c)
        tmp_1 = np.uint32((np.uint64(h) + np.uint64(x_1) + np.uint64(ch) + np.uint64(K[i]) + np.uint64(W[i])) % 2**32)
        tmp_2 = np.uint32((np.uint64(x_2) + np.uint64(maj)) % 2**32)
        h = g
        g = f
        f = e
        e = np.uint32((np.uint64(d) + np.uint64(tmp_1)) % 2**32)
        d = c
        c = b
        b = a
        a = np.uint32((np.uint64(tmp_1) + np.uint64(tmp_2)) % 2**32)
    H = []
    H.append(np.uint32((np.uint64(R[0]) + np.uint64(a)) % 2**32))
    H.append(np.uint32((np.uint64(R[1]) + np.uint64(b)) % 2**32))
    H.append(np.uint32((np.uint64(R[2]) + np.uint64(c)) % 2**32))
    H.append(np.uint32((np.uint64(R[3]) + np.uint64(d)) % 2**32))
    H.append(np.uint32((np.uint64(R[4]) + np.uint64(e)) % 2**32))
    H.append(np.uint32((np.uint64(R[5]) + np.uint64(f)) % 2**32))
    H.append(np.uint32((np.uint64(R[6]) + np.uint64(g)) % 2**32))
    H.append(np.uint32((np.uint64(R[7]) + np.uint64(h)) % 2**32))
    return H

def pretty_print(msg: str):
    print(f"""
----------------------------------------------------------------------------------------------
Message:    {msg}

Digest:     {sha256(msg)}
----------------------------------------------------------------------------------------------
""")

print("""
SHA256 Implementation

==============================================================================================

Example 1""")
pretty_print(ex1)
print("Example 2")
pretty_print(ex2)
print("Example 3")
pretty_print(ex3)

def int64tostr(number: int = 5) -> str:
    binary = format(number, '064b')
    list_chars = [binary[i: i + 8] for i in range(0, len(binary), 8)]
    string = [chr(int(i, 2)) for i in list_chars]
    return "".join(i for i in string)

import hashlib

def proof_of_work(name: str = "Donnet"):
    number = 0
    while number <= 2**64 - 1:
        # Using my sha256 function doesn't work...
        # digest = sha256(name + int64tostr(number))
        digest = hashlib.sha256((name + int64tostr(number)).encode('utf-8')).hexdigest()
        if digest[-5:] == "00000":
            return digest, number
        number += 1
    print("Not found")

print(proof_of_work())
