from SHAConstants import *
import numpy as np


def join_table(table: list = ["t", "e", "s", "t"]) -> str:
    """
    Function that join all elements of a character/string table to a string

    Parameters
    ----------
    table : list of characters/string


    Returns
    -------
    str : final string


    """
    return "".join(i for i in table)


def block2int(binary: str) -> np.ndarray:
    """
    Function that convert a binary string to 32-bits integer

    Parameters
    ----------
    binary : str


    Returns
    -------
    np.ndarray of 32-bits integer

    """
    binaries_list = [join_table(binary[i : i + 32]) for i in range(0, len(binary), 32)]
    uint32_list = [np.uint32(int(i, 2)) for i in binaries_list]
    return np.array(uint32_list)


def rotate(binary: int, shift: int, left: bool = False) -> int:
    """
    Function that make a cyclic binary rotation

    Parameters
    ----------
    binary : int
        The binary is in form of integer.

    shift : int
        Shift we want to achieve

    left : bool
        Direction of the shift

    Returns
    -------
    int : the binary with the rotation completed

    """
    shifted = np.array(list(format(binary, "032b")))
    assert shift <= len(shifted), "Shift must be <= number of bits !"
    if left:
        shifted = np.concatenate((shifted[shift:], shifted[:shift]))
    else:
        shifted = np.concatenate((shifted[-shift:], shifted[:-shift]))
    return np.uint32(int(join_table(shifted), 2))


def padding(msg: str = "coucou") -> str:
    """
    Function that convert a string to bits and add a padding with the length of the string to have a final bit sequence multiple of 512

    Parameters
    ----------
    msg : str
        The initial message on string form


    Returns
    -------
    str
        The string of bits that represent the message + 1 + padding + length

    """
    tmp = [format(ord(i), "08b") for i in msg]
    binary = join_table(tmp)
    length = format(len(binary), "064b")
    binary += "1"
    current_length = len(length) + len(binary)
    K = 512 * (current_length // 512 + 1) - current_length
    binary += "0" * K + length
    return binary


def sha256(msg: str = "coucou") -> str:
    """
    Compute the sha256 of the given message

    Parameters
    ----------
    msg : str
        The message string

    Returns
    -------
    str
        Result on form string of hexadecimal characters

    """
    # Padding message
    binary = padding(msg)
    binary = np.array(list(binary))
    # Split binary sequence in block of 512 bits
    binary = binary.reshape(-1, 512)
    # If we have only 1 block, convert binary to 2D array
    if len(binary.shape) == 1:
        binary = np.array([binary])
    assert len(binary.shape) == 2, "Table of binary must be 2D !"
    # Initialize the factor added to the computation
    R = list(IV)
    for i in range(len(binary)):
        # Compute each block and update R factor for each new computation
        R = one_way(binary[i], R)
    # The last R is the digest
    # Format result to hexadecimal string
    result = "".join(i for i in [hex(j) for j in R])
    return result


def one_way(binary: str, R: list[np.uint32]) -> list[np.uint32]:
    """
    Function that create a list of 64 words of 32 bits and compress it to an output of 256 bits

    Parameters
    ----------
    R :
        Factor that is added to the computation of the compression

    binary : str
        Block of 512 bits to look after

    Returns
    -------
    list[np.uint32]:
        Output of the compression of 256 bits of the 64 words

    """
    assert len(binary) == 512, f"Len of binary must be 512 ! actual {len(binary)}"
    # We work here with list of int32 !
    W = list(block2int(binary))
    rotate(W[0], 3, True)
    for i in range(16, 64):
        s_0 = rotate(W[i - 15], 7) ^ rotate(W[i - 15], 18) ^ (W[i - 15] >> 3)
        s_1 = rotate(W[i - 2], 17) ^ rotate(W[i - 2], 19) ^ (W[i - 2] >> 10)
        # We must convert to int64 to avoid overflow in manipulations, and then reconvert to int32
        W.append(
            np.uint32(
                (
                    np.int64(W[i - 16])
                    + np.int64(s_0)
                    + np.int64(W[i - 7])
                    + np.int64(s_1)
                )
                % 2**32
            )
        )
    assert len(W) == 64, "Len of W must be 64 !"
    return compression(W, R)


def compression(W: list[np.uint32], R: list[np.uint32]) -> list[np.uint32]:
    """
    Function that achieve the compression of the list of 64 words of 32 bits to an output of 256 bits depending on the factor R

    Parameters
    ----------
    W : list[np.uint32]
       List of the 64 words of 32 bits

    R : list[np.uint32]
       Factor used to compute output

    Returns
    -------
        list[np.uint32]:
            The compressed output

    """
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
        tmp_1 = np.uint32(
            (
                np.uint64(h)
                + np.uint64(x_1)
                + np.uint64(ch)
                + np.uint64(K[i])
                + np.uint64(W[i])
            )
            % 2**32
        )
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
    """
    Function that print message and digest from message using our sha256 implementation

    Parameters
    ----------
    msg : str
        The message to compute

    """
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


# ============================================================================================
#
#                                   PROOF OF WORK
#
# ============================================================================================


print("""
==============================================================================================

                                    PROOF OF WORK

==============================================================================================
""")


def int64tostr(number: int = 5) -> str:
    """
    Convert a int64 to 2 char (usefull to add it at the end of my string)

    Parameters
    ----------
    number : int
        Number to convert

    Returns
    -------
    str
        The sequence of chars that encode the number

    """
    binary = format(number, "064b")
    list_chars = [binary[i : i + 8] for i in range(0, len(binary), 8)]
    string = [chr(int(i, 2)) for i in list_chars]
    return "".join(i for i in string)


def proof_of_work(name: str = "donnet"):
    """
    Iterate on sha256 computations of name with an int64 added to have a hexadecimal digest that finish with 5 '0'
    In my case, it works only until 3 '0'.

    Parameters
    ----------
    name : str
        Name to compute

    """
    number = 0
    while number <= 2**64 - 1:
        digest = sha256(name + int64tostr(number))
        # Using my sha256 function it works only with 3 '0'
        if digest[-3:] == "000":
            print(f"""
----------------------------------------------------------------------------------------------
Digest:     {digest}

Number of iterations:   {number}
----------------------------------------------------------------------------------------------
""")
            return
        number += 1
    print("Not found")


proof_of_work()
