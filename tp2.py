import numpy as np
from Sboxes_and_examples import message, key, key2, key3, Sbox, Sbox_inv


class AES:
    def str2bytes(self, param: str) -> bytes:
        return param.encode("utf-8")

    def bytes2bits(self, param: bytes) -> str:
        return "".join(format(b, "08b") for b in param)

    def str2bits(self, param: str) -> str:
        return "".join(format(b, "08b") for b in param.encode("utf-8"))

    def int2bits(self, param: int) -> str:
        return format(param, "08b")

    def bits2int(self, param: str) -> int:
        return int(param, 2)

    def bits2listint(self, param: str) -> list[int]:
        assert len(param) // 8 == len(param) / 8, (
            "To convert a list of bits to list of int, you must have multiple of 8 bits !"
        )
        return [int(param[i : i + 8], 2) for i in range(0, len(param), 8)]

    def listbits2hex():
        pass

    def padding(self, param: str) -> list[str]:
        list_bits = self.str2bits(param)
        L = len(list_bits) // 8
        X = 16 - L % 16
        pad = "".join(format(0, "08b") for _ in range(int(X - 1)))
        pad += format(X, "08b")
        list_bits += pad
        assert len(list_bits) // 128 == len(list_bits) / 128, (
            f"After padding, number of bits must be a multiple of 128 ! Current number of bits: {len(list_bits)}"
        )
        return [list_bits[i : i + 128] for i in range(0, len(list_bits), 128)]

    def shift(self, M: np.ndarray):
        return np.array([np.roll(M[i], -i) for i in range(M.shape[0])])

    def encrypt_box(self, plaintext: str, encrypt_key: str):
        assert len(plaintext) == 128, "You must provide a plaintext of 128 bits !"
        M = np.array(self.bits2listint(plaintext)).reshape(4, 4).T
        W = self.key_expansion(encrypt_key)
        print(W.shape)
        N = len(self.bits2listint(self.str2bits(encrypt_key))) + 6
        M ^= W[:4]
        shift = np.array([np.roll(np.arange(4), -i) for i in range(4)]).astype(int)
        print(f"Shift matrix: {shift}")
        for i in range(N):
            M = self.replacement(np.array(Sbox), M)
            print(M.shape)
            M = self.shift(M)
            print(M.shape)
            if i < N - 1:
                print("MixColumn")
                GF = np.array([2, 3, 1, 1])
                GF = GF[shift]
                M = self.mixColumn(GF, M)
            M ^= W[i]
        return "".join(format(i, "02x") for i in M.T.ravel())

    def int2poly(self, param: int) -> np.ndarray:
        return np.array(list(format(int(param), "08b"))).astype(int)

    def polymul(self, p1: np.ndarray, p2: np.ndarray) -> int:
        result = np.convolve(p1, p2) % 2
        return int("".join(str(b) for b in result), 2)

    def mixColumn(self, GF: np.ndarray, M: np.ndarray) -> np.ndarray:
        r = int("100011011", 2)
        print(f"r: {r}")
        for k in range(M.shape[1]):
            for j in range(M.shape[0]):
                result = 0
                p = self.int2poly(M[j, k])
                for i in range(GF.shape[0]):
                    p1 = self.int2poly(GF[j, i])
                    result ^= self.polymul(p, p1)
                M[j, k] = result % r
        return M

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

    def replacement(self, SBox: np.ndarray, param: np.ndarray) -> np.ndarray:
        index = (param % 16) + 16 * (param // 16)
        print(f"Param: {param}")
        print(f"index: {index}")
        return SBox[index.astype(int)]

    def key_expansion(self, param: str):
        K = self.bits2listint(self.str2bits(param))
        assert len(K) == 4 or len(K) == 6 or len(K) == 8, (
            f"Key must have 4, 6 or 8 32bits words ! Actual: {len(K)}"
        )
        rcon = self.constants()
        N = len(K)
        if N == 4:
            R = 11
        elif N == 6:
            R = 13
        else:
            R = 15
        W = np.zeros((4 * R, 4)).astype(int)
        for i in range(4 * R):
            if i < N:
                W[i] = K[i]
            elif i % N == 0:
                W[i] = (
                    W[i - N]
                    ^ self.replacement(np.array(Sbox), np.roll(W[i - 1], -1))
                    ^ rcon[i // N]
                )
            elif i % N == 4:
                W[i] = W[i - N] ^ self.replacement(np.array(Sbox), W[i - 1])
            else:
                W[i] = W[i - N] ^ W[i - 1]
        return W

    def aes(self, plaintext: str, encrypt_key: str):
        blocks = self.padding(plaintext)
        result = ""
        for block in blocks:
            result += self.encrypt_box(block, encrypt_key)


test = AES()
test.encrypt_box(test.padding("Blalalaskdjflkasjdflksajflksadjflkjl")[0], "blabla")

print(test.aes(message, key2))
