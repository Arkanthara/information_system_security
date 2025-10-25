import numpy as np
from Sboxes_and_examples import message, key, key2, key3, Sbox, Sbox_inv


class AES:
    def str2bits(self, param: str) -> str:
        """
        Convert a string to bit sequence

        Parameters
        ----------
        param : str
            string to convert

        Returns
        -------
        str
            bit sequence on string form

        """
        return "".join(format(b, "08b") for b in param.encode("utf-8"))

    def int2bits(self, param: int) -> str:
        """
        Convert a integer to bit sequence

        Parameters
        ----------
        param : int
            integer to convert

        Returns
        -------
        str
            bit sequence on string form

        """
        return format(param, "08b")

    def bits2listint(self, param: str) -> list[int]:
        """
        Convert a bit string to a list of integers 8 bits

        Parameters
        ----------
        param : str
            bit sequence to convert

        Returns
        -------
        list[int]
            List of integers

        """
        assert len(param) // 8 == len(param) / 8, (
            "To convert a list of bits to list of int, you must have multiple of 8 bits !"
        )
        return [int(param[i : i + 8], 2) for i in range(0, len(param), 8)]

    def int2poly(self, param: int) -> np.ndarray:
        """
        Convert an integer to a polynom represented on list form with coefficients.
        For instance, 3 will give polynom [0, 0, 0, 0, 0, 1, 1, 1]

        Parameters
        ----------
        param : int
            Integer to convert

        Returns
        -------
        np.ndarray
            polynom coefficients

        """
        return np.array(list(format(int(param), "08b"))).astype(int)

    def polymodulo(self, p: np.ndarray) -> np.ndarray:
        """
        Compute modulo of given polynom with Rijndael polynom.
        To perform the modulo, a simple polynom division is made.

        Parameters
        ----------
        p : np.ndarray
            polynom to compute modulo

        Returns
        -------
        np.ndarray
            result of the modulo

        """
        r = np.array([1, 0, 0, 0, 1, 1, 0, 1, 1])
        while len(p) >= len(r):
            if p[0] == 1:
                p[: len(r)] ^= r
            p = p[1:]
        assert len(p) == len(r) - 1, f"p must be of length r - 1 ! Current: {len(p)}"
        return p

    def polymul(self, p1: np.ndarray, p2: np.ndarray) -> np.ndarray:
        """
        Perform a polynom multiplication between polynom p1 and p2

        Parameters
        ----------
        p1 : np.ndarray
            polynom 1
        p2 : np.ndarray
            polynom 2

        Returns
        -------
        np.ndarray
            return the polynom multiplication

        """
        result = np.convolve(p1, p2) % 2
        return self.polymodulo(result)

    def shift(self, M: np.ndarray, right: bool = False) -> np.ndarray:
        """
        Perform shift on M matrix with first row left intact, second row left shifted 1 time, third row left shifted 2 times, ...
        If right is true, perform right shifts.

        Parameters
        ----------
        M : np.ndarray
            Matrix to perform the shifts on rows
        right: bool
            Right direction indicator

        Returns
        -------
        np.ndarray
            return the shifted matrix

        """
        if right:
            return np.array([np.roll(M[i], i) for i in range(M.shape[0])])
        return np.array([np.roll(M[i], -i) for i in range(M.shape[0])])

    def replacement(self, SBox: np.ndarray, param: np.ndarray) -> np.ndarray:
        """
        Perform substitution according to the SBox matrix

        Parameters
        ----------
        SBox : np.ndarray
            Sbox matrix to give values for substitution
        param : np.ndarray
            Index for substitution

        Returns
        -------
        np.ndarray
            Values substitued

        """
        index = (param % 16) + 16 * (param // 16)
        return SBox[index.astype(int)]

    def constants(self) -> np.ndarray:
        """
        Create matrix of constants used for key generation

        Returns
        -------
        np.ndarray
            matrix of constants

        """
        rcon = np.zeros((10, 4))

        table = [
            "0x01",
            "0x02",
            "0x04",
            "0x08",
            "0x10",
            "0x20",
            "0x40",
            "0x80",
            "0x1B",
            "0x36",
        ]
        for i in range(len(table)):
            rcon[i, 0] = int(table[i], 16)
        return rcon.astype(int)

    def padding(self, param: str) -> list[str]:
        """
        Convert a string to bit sequence and apply padding.
        Return blocks of size multiple of 128

        Parameters
        ----------
        param : str
            string to convert

        Returns
        -------
        list[str]
            sequence of bits divided in blocks of 128 bits

        """
        list_bits = self.str2bits(param)
        L = len(list_bits) // 8
        X = 16 - L % 16
        pad = "".join(format(X, "08b") for _ in range(int(X)))
        list_bits += pad
        assert len(list_bits) // 128 == len(list_bits) / 128, (
            f"After padding, number of bits must be a multiple of 128 ! Current number of bits: {len(list_bits)}"
        )
        return [list_bits[i : i + 128] for i in range(0, len(list_bits), 128)]

    def mixColumn(self, GF: np.ndarray, M: np.ndarray) -> np.ndarray:
        """
        Perform mix column operation of AES algorithm

        Parameters
        ----------
        GF : np.ndarray
            Matrix of polynoms
        M : np.ndarray
            Initial matrix to convert with mix column operation

        Returns
        -------
        np.ndarray
            Matrix with mix column operation applied

        """
        mixColumn_result = np.zeros_like(M)
        for k in range(M.shape[1]):
            for j in range(M.shape[0]):
                result = np.zeros(8).astype(int)
                for i in range(GF.shape[0]):
                    p1 = self.int2poly(GF[j, i])
                    p2 = self.int2poly(M[i, k])
                    result ^= self.polymul(p2, p1)
                mixColumn_result[j, k] = int("".join(str(b) for b in result), 2)
        return mixColumn_result

    def key_expansion(self, param: str) -> np.ndarray:
        """
        Perform key expansion for the given key string 'param'

        Parameters
        ----------
        param : str
            key to expand

        Returns
        -------
        np.ndarray
            Expanded key

        """
        K = self.bits2listint(self.str2bits(param))
        N = len(K) // 4
        assert N == 4 or N == 6 or N == 8, (
            f"Key must have 4, 6 or 8 32bits words ! Actual: {len(K)}"
        )
        rcon = self.constants()
        if N == 4:
            R = 11
        elif N == 6:
            R = 13
        else:
            R = 15
        W = np.zeros((4 * R, 4)).astype(int)
        for i in range(4 * R):
            if i < N:
                W[i] = K[4 * i : 4 * (i + 1)]
            elif i % N == 0:
                W[i] = (
                    W[i - N]
                    ^ self.replacement(np.array(Sbox), np.roll(W[i - 1], -1))
                    ^ rcon[i // N - 1]
                )
            elif i % N == 4 and N > 6:
                W[i] = W[i - N] ^ self.replacement(np.array(Sbox), W[i - 1])
            else:
                W[i] = W[i - N] ^ W[i - 1]
        return W

    def encrypt_box(self, plaintext: str, encrypt_key: str) -> str:
        """
        AES encryption box that perform encryption on blocks according to encrypt key given

        Parameters
        ----------
        plaintext : str
            plaintext given
        encrypt_key : str
            encrypt key given

        Returns
        -------
        str:
            ciphertext computed

        """
        assert len(plaintext) == 128, "You must provide a plaintext of 128 bits !"
        M = np.array(self.bits2listint(plaintext)).reshape(4, 4).T
        W = self.key_expansion(encrypt_key)
        N = W.shape[0] // 4
        M ^= W[:4].T
        for i in range(1, N):
            M = self.replacement(np.array(Sbox), M)
            # Test for shift
            # assert np.array_equal(
            #     self.shift(np.array([[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]])),
            #     np.array([[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1]]),
            # )
            M = self.shift(M)
            if i < N - 1:
                GF = np.array([[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]])
                M = self.mixColumn(GF, M)
            M ^= W[4 * i : 4 * (i + 1)].T
        return "".join(format(i, "02x") for i in M.T.ravel())

    def decrypt_box(self, ciphertext: str, encrypt_key: str) -> str:
        """
        AES decryption box that perform encryption on blocks according to encrypt key given

        Parameters
        ----------
        ciphertext : str
            plaintext given
        encrypt_key : str
            encrypt key given

        Returns
        -------
        str:
            plaintext decrypted

        """
        assert len(ciphertext) == 128, "You must provide a ciphertext of 128 bits !"
        M = np.array(self.bits2listint(ciphertext)).reshape(4, 4).T
        W = self.key_expansion(encrypt_key)[::-1]
        N = W.shape[0] // 4
        M ^= W[:4].T
        for i in range(1, N):
            M = self.replacement(np.array(Sbox_inv), M)
            # Test for shift
            # assert np.array_equal(
            #     self.shift(np.array([[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]])),
            #     np.array([[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1]]),
            # )
            M = self.shift(M, right=True)
            if i < N - 1:
                GF = np.array(
                    [
                        [0x0E, 0x0B, 0x0D, 0x09],
                        [0x09, 0x0E, 0x0B, 0x0D],
                        [0x0D, 0x09, 0x0E, 0x0B],
                        [0x0B, 0x0D, 0x09, 0x0E],
                    ]
                )
                M = self.mixColumn(GF, M)
            M ^= W[4 * i : 4 * (i + 1)].T
        return "".join(chr(i) for i in M.T.ravel())

    def encode(self, plaintext: str, encrypt_key: str):
        """
        AES encodage of a plaintext given the encrypt_key

        Parameters
        ----------
        plaintext : str
            plaintext to encode
        encrypt_key : str
            encrypt_key used for encodage

        Returns
        -------
        str:
            ciphertext computed (for each block of AES)

        """
        print("======= ENCRYPTION ========\n")
        print("======== PLAINTEXT ========\n")
        print(f"Plaintext: {plaintext}\n")
        print("=========== KEY ===========\n")
        print(f"Key: {key}\n")
        blocks = self.padding(plaintext)
        result = ""
        for block in blocks:
            result += self.encrypt_box(block, encrypt_key) + "\n"
        print("======= CIPHERTEXT ========\n")
        print(f"Ciphertext: {result}\n")
        print("===========================\n\n")
        return result

    def decode(self, ciphertext: str, encrypt_key: str):
        """
        AES decodage of a ciphertext given the encrypt_key

        Parameters
        ----------
        ciphertext : str
            ciphertext to decode
        encrypt_key : str
            encrypt_key used for encodage

        Returns
        -------
        str:
            plaintext computed (for each block of AES)

        """
        print("======= DECRYPTION ========\n")
        print("======= CIPHERTEXT ========\n")
        print(f"Ciphertext: {ciphertext}\n")
        print("=========== KEY ===========\n")
        print(f"Key: {key}\n")
        blocks = self.padding(ciphertext)
        result = ""
        for block in blocks:
            result += self.decrypt_box(block, encrypt_key) + "\n"
        print("======== PLAINTEXT ========\n")
        print(f"Plaintext: {result}\n")
        print("===========================\n\n")
        return result


aes = AES()

test = aes.encode(message, key)
aes.decode(test, key)
test = aes.encode(message, key2)
aes.decode(test, key2)
test = aes.encode(message, key3)
aes.decode(test, key3)
