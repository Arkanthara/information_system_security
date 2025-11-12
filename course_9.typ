== General Problems

- Factorize
- Discret Logarithm Problem (DLP)
- Square Root Problem (SQROOTP)

== Specific problems

- RSA (RSAP)
- Diffie-Hellman (DHP) we have $alpha^a$ and $alpha^b$ and we want to find $alpha^(a b)$

== RSA

Keep p and q ! It allows a faster computation of modulo (so faster encryption and decryption !)
RSA is multiplicative homomorphism: $(m_1m_2)^e = m_1^e m_2^e = c_1 c_2 mod n$

== ElGamal

- Work with big prime number $p$ and a generator $alpha$ of multiplicative group of $p$
- Generate secret number $a in {2, p - 2}$
- Private key is $a$
- Public key is $(p, alpha, alpha^a mod p)$

=== Encrypt

- Generate random number $k$
- Send $(alpha^k mod p, m_i (alpha^a mod p)^k mod p)$

=== Decrypt

- Compute $lambda^(p - 1 - a) mod p = lambda^(-a) = alpha^(-a k) mod p$ according to Euler theorem: $alpha^(p - 1) = 1 mod p$
- Retrieve message: $alpha^(-a k) delta mod p = m_i alpha^(-a k + a k) mod p = m_i$

=== Advantage

$k$ mask deterministic and small entropy of the message.
If we encode message multiple time, we will have always different ciphertexts due to the $k$

== Elliptic curves

- Define a curve $y^2 = x^3 + a x + b$
- Define sum as $P + Q = R$. Note: $P + (-P) = infinity$
- Define multiplication as taking tangent to the curve: $P + P = 2P = R$. 

Why using this ???
We can have a very strong security with smaller keys compared to RSA for ASYMETRIC cryptography

=== ElGamal

- Public key is elliptic curve $E_p$, starting point $P_0$ and $P_a$ the result of how many times we multiply $P_0$.
- Private key is how many time we multiply $P_0$.

