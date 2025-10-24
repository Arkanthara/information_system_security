import numpy as np
from Sboxes_and_examples import message, key, key2, key3, Sbox, Sbox_inv


class AES:
    def str2bits(self, param: str) -> str:
        return "".join(format(b, "08b") for b in param.encode("utf-8"))

    def int2bits(self, param: int) -> str:
        return format(param, "08b")

    def bits2listint(self, param: str) -> list[int]:
        assert len(param) // 8 == len(param) / 8, (
            "To convert a list of bits to list of int, you must have multiple of 8 bits !"
        )
        return [int(param[i : i + 8], 2) for i in range(0, len(param), 8)]

    def int2poly(self, param: int) -> np.ndarray:
        return np.array(list(format(int(param), "08b"))).astype(int)

    def polymodulo(self, p: np.ndarray) -> np.ndarray:
        r = np.array([1, 0, 0, 0, 1, 1, 0, 1, 1])
        while len(p) >= len(r):
            if p[0] == 1:
                p[: len(r)] ^= r
            p = p[1:]
        assert len(p) == len(r) - 1, f"p must be of length r - 1 ! Current: {len(p)}"
        return p

    def polymul(self, p1: np.ndarray, p2: np.ndarray) -> np.ndarray:
        result = np.convolve(p1, p2) % 2
        return self.polymodulo(result)

    def shift(self, M: np.ndarray):
        return np.array([np.roll(M[i], -i) for i in range(M.shape[0])])

    def replacement(self, SBox: np.ndarray, param: np.ndarray) -> np.ndarray:
        index = (param % 16) + 16 * (param // 16)
        return SBox[index.astype(int)]

    def constants(self) -> np.ndarray:
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

    def key_expansion(self, param: str):
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

    def encrypt_box(self, plaintext: str, encrypt_key: str):
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

    def encode(self, plaintext: str, encrypt_key: str):
        print(f"Plaintext: {plaintext}")
        print(f"Key: {key}")
        blocks = self.padding(plaintext)
        result = ""
        for block in blocks:
            result += self.encrypt_box(block, encrypt_key) + "\n"
        return result


test = AES()

print(test.encode("Two One Nine Two", "Thats my Kung Fu"))
print(test.encode(message, key))
print(test.encode(message, key2))
print(test.encode(message, key3))
