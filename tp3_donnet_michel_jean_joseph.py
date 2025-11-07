import numpy as np
import random
import hashlib
from TP3examples import *

def fast_exp(a: int, p: int, n: int) -> int:
    """
    Apply fast exponentiation for a^p modulo n

    Parameters
    ----------
    a : int
        Number
    p : int
        Power
    n : int
        Modulo

    Returns
    -------
    int
        Result of fast exponentiation

    """
    binary = np.array(list(format(p, "0b"))).astype(int)[::-1]
    if binary.shape[0] == 1:
        return a**p % n
    power_of_2 = np.zeros_like(binary, dtype=object)
    power_of_2[0] = a % n
    for i in range(1, power_of_2.shape[0]):
        power_of_2[i] = (power_of_2[i - 1] ** 2) % n
    result = 1

    for i in range(power_of_2.shape[0]):
        if binary[i] == 1:
            result = (result * power_of_2[i]) % n
    return result

def fermat_test(n: int) -> bool:
    """
    Check if a number is primary by running Fermat test.

    Parameters
    ----------
    n : int
        Number to check

    Returns
    -------
    bool
        True if the number is primary

    """
    for i in range(20):
        alpha = random.randint(2, n - 1)
        if fast_exp(alpha, n - 1, n) != 1:
            return False
    return True


def primary_nb_generator(a: int, b: int) -> int:
    """
    Generate primary number in range a, b

    Parameters
    ----------
    a : int
        lower bound
    b : int
        upper bound

    Returns
    -------
    int
        Primary number generated

    """
    while True:
        p = random.randint(a, b)
        if fermat_test(p):
            return p


def Euclide(a: int, b: int) -> list:
    """
    Euclide's extended algorithm, used to find decryption exponent d for RSA

    Parameters
    ----------
    a : int
        Number
    b : int
        Number

    Returns
    -------
    list
        A list [pgcd(a, b), inverse of a mod b, inverse of b mod a]

    """
    assert a >= b, "a must be greater than b !"
    r_0, r_1 = a, b
    s_0, s_1 = 1, 0
    t_0, t_1 = 0, 1
    q_1 = r_0 // r_1
    while r_1 != 0:
        r_0, r_1 = r_1, r_0 - q_1 * r_1
        s_0, s_1 = s_1, s_0 - q_1 * s_1
        t_0, t_1 = t_1, t_0 - q_1 * t_1
        if r_1 != 0:
            q_1 = r_0 // r_1
    tab = [r_0]
    tab.append(s_0 if s_0 >= 0 else s_0 + b)
    tab.append(t_0 if t_0 >= 0 else t_0 + a)
    return tab


def key_generator(p: int = 0, q: int = 0, e: int = 0) -> list:
    """
    Generate public and private key for RSA

    Returns
    -------
    list
        modulo, public, private key

    """
    if p == 0:
        p = primary_nb_generator(2**511, 2**512)
    if q == 0:
        q = primary_nb_generator(2**511, 2**512)

    assert fermat_test(p), "p is not primary"
    assert fermat_test(q), "q is not primary"
    n = p * q
    phi_n = (p - 1) * (q - 1)

    if e != 0:
        pgcd, _, d = Euclide(phi_n, e)
        assert pgcd == 1, "pgcd(phi_n, e) is not equal to 1, so no private key found !"

    else:
        # Find a primary number e with phi_n
        while True:
            e = random.randint(2**511, 2**512)
            pgcd, _, d = Euclide(phi_n, e)

            # If primary number with phi_n, claim public key
            if pgcd == 1:
                break
    return n, e, d


def get_digest(message: int) -> str:
    # Ensure upper round is made with the +7
    size = (message.bit_length() + 7) // 8
    message_in_bytes = message.to_bytes(size, 'big')
    return hashlib.sha256(message_in_bytes).hexdigest()


def signature(message: int, d: int, n: int) -> int:
    digest = get_digest(message)
    return fast_exp(int(digest, base=16), d, n)

def check_signature(message: int, signature: int, e: int, n: int) -> bool:
    digest = int(get_digest(message), 16)
    sign = fast_exp(signature, e, n)
    if digest == sign:
        print("Signature verified !")
        return True
    return False

if __name__ == "__main__":
    print("\n=============== RSA ENCRYPTION ===============\n")

    n, e, d = key_generator(p_A, q_A, e_A)
    assert d == d_A, "Private key generated is different from the expected key !"

    print(f"Message:                {m_1}\n")

    cipher = fast_exp(m_1, e, n)
    assert cipher == 32468932964181322647810913060097066975304467072050643211304428656476623133068329653886195740426516038144100129255895281039142864272296799126753030014464755203797098445143314298922512718785433009136404533290100525054356166805463645892708927694801117827432767298393815743170470207262077229267156532545837844746, "Encrypted message is not correct !"
    print(f"Ciphertext:             {cipher}\n")

    recovered_message = fast_exp(cipher, d, n)
    assert recovered_message == m_1, "Recovered message is different from original message !"
    print(f"Decrypted ciphertext:   {recovered_message}")

    print("\n=============== RSA SIGNATURE ===============\n")
    
    print(f"Message:                {m_2}\n")

    m_2_signed = signature(m_2, d_B, n_B)
    assert m_2_signed == 139946149260693867607112906574735868062749437621729152371217474062708529251204743665018991444038005832618912915250036414898959900238801293242485481120544999182886616669733899259575955678176133539745600054828147224713714471521374309679085794180533135483883902152178064817185104702608162450188184338147593819800, "Signature is not correct !"
    print(f"Signature:              {m_2_signed}\n")

    check_signature(m_2, m_2_signed, e_B, n_B)


