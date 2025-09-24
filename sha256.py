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
    binary.reshape(-1, 512)
    if len(binary.shape) == 1:
        binary = np.array([binary])
    assert len(binary.shape) == 2, "Table of binary must be 2D !"
    one_way(binary[0])
    
def one_way(binary: str):
    assert len(binary) == 512, "Len of binary must be 512 !"
    W = list(block2int(binary))
    rotate(W[0], 3, True)
    for i in range(16, 64):
        s_0 = rotate(W[i - 15], 7) ^ rotate(W[i - 15], 18) ^ (W[i - 15] >> 3)    # Possibly change the value of 15 to 14 because python indexing...
        s_1 = rotate(W[i - 2], 17) ^ rotate(W[i - 2], 19) ^ (W[i - 2] >> 10)
        W.append(np.uint32((np.int64(W[i - 16]) + np.int64(s_0) + np.int64(W[i - 7]) + np.int64(s_1)) % 2**32))
    assert len(W) == 64, "Len of W must be 64 !"

sha256()
