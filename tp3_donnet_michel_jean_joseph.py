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


def primary_nb_generator(a: int, b: int, safe_prime: bool = False) -> int:
    """
    Generate primary number in range a, b

    Parameters
    ----------
    a : int
        lower bound
    b : int
        upper bound
    safe_prime : bool
        Generate primary number p with (p - 1) / 2 also primary

    Returns
    -------
    int
        Primary number generated

    """
    while True:
        p = random.randint(a, b)
        if fermat_test(p):
            if safe_prime:
                if fermat_test((p - 1) / 2):
                    return p
            else:
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
    """
    Return sha256 digest from the given message

    Parameters
    ----------
    message : int
        Message

    Returns
    -------
    str
        sha256 digest

    """
    # Ensure upper round is made with the +7
    size = (message.bit_length() + 7) // 8
    message_in_bytes = message.to_bytes(size, 'big')
    return hashlib.sha256(message_in_bytes).hexdigest()


def signature(message: int, key: int, n: int) -> int:
    """
    Sign the give message with the given key (key, n)

    Parameters
    ----------
    message : int
        Message
    key : int
        Key used to sign message
    n : int
        Modulo corresponding to the given key

    Returns
    -------
    int
        The message signed

    """
    digest = get_digest(message)
    return fast_exp(int(digest, base=16), key, n)

def check_signature(message: int, signature: int, key: int, n: int) -> bool:
    """
    Check integrity of given message according to signature

    Parameters
    ----------
    message : int
        check integrity of message
    signature : int
        signature used to check integrity of message
    key : int
        key used to decrypt signature
    n : int
        modulo corresponding to the given key

    Returns
    -------
    bool
        True if integrity of message is configured

    """
    digest = int(get_digest(message), 16)
    sign = fast_exp(signature, key, n)
    if digest == sign:
        print("Signature verified !")
        return True
    print("Signature not verified !")
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

    print("\n\n============= STATION-TO-STATION ============\n")

    print(f"Alice to Bob\n")
    ax = fast_exp(alpha, x, safe_prime)
    assert ax == 686072914171234798069517712764277594421530837248520761454562297567737629274501846654087857110320672185192257738624560988240804394506647168646502643636056310, "Secret a^x mod p not correct !"
    print(f"a^x mod p:  {ax}\n")

    print("Bob to Alice\n")
    ay = fast_exp(alpha, y, safe_prime)
    K1 = fast_exp(ax, y, safe_prime)
    assert ay == 1658758911043428653679670657159403893659858431555423238518923992311175752537434444470667284622227826513095646428663996761247179634768488071743521322105826864, "Secret a^y mod p not correct !"
    assert K1 == 133319045406894848338625909766918081728670119580456005459847062820377364927299550101232531204505214272971383981615061959224396184823089732799942062031596841, "Session key K is not correct !"
    SB_key = signature(int(format(ax, '0b') + format(ay, '0b') + format(K1, '0b'), 2), d_B, n_B)
    assert SB_key == 63637939875901691094764242278906665544983903077054207988218710640087544761228273045150821483357729338737390290548046762350697337909101721771119707350314342587290126983794881205873189463125171775729781807366888186695684820979887485019292913876833243417638388536805972736525678021591270150561199609942649208004, "Signature from Bob on (alpha^x, alpha^y, K) is not correct !"
    print(f"a^y mod p:  {ay}\n")
    print(f"Signature:  {SB_key}\n")

    print(f"Alice to Bob\n")
    K2 = fast_exp(ay, x, safe_prime)
    assert K2 == 133319045406894848338625909766918081728670119580456005459847062820377364927299550101232531204505214272971383981615061959224396184823089732799942062031596841, "Session key K is not correct !"
    check_signature(int(format(ax, '0b') + format(ay, '0b') + format(K2, '0b'), 2), SB_key, e_B, n_B)
    print()
    SA_key = signature(int(format(ay, '0b') + format(ax, '0b') + format(K2, '0b'), 2), d_A, n_A)
    assert SA_key == 45467152564432701103620506688535942942709188195272432989568457473601022575230584678514742692432145004914876272400870285574876815019240848540253393082439483176306291410816134069425004279929786767259112836051752427213131534826834152132670963428804617973787768260686245775875564276853832786703782164483812397373, "Signature from Alice on (alpha^y, alpha^x, K) is not correct !"
    print(f"Signature:  {SA_key}\n")

    print("Bob\n")
    check_signature(int(format(ay, '0b') + format(ax, '0b') + format(K1, '0b'), 2), SA_key, e_A, n_A)
    print()

    print("\n---------------- Session key ----------------\n")
    print(K1)
    print("\n-------------------- END --------------------\n")






