== Block Ciphers

=== Diferencial cryptanalysis

- choosen plaintext attack that see difference propagation in 2 plaintexts in different state of the algorithm
- give probability to predicted keys depending on changes. After a lot of plaintext/ciphertext, the key has a lot of chances to be the correct key
- need $2^{47}$ couples choosen plaintexts

=== Linear cryptanalysis

- known plaintext attack that simulate behavior of blocks according to linear approximations with lot of data
- For DES, need $2^{38}$ known plaintexts to have 10% chances of success
- It's the stronger analysis attack on block ciphers...

=== Notes

- It presents difficulties in parallelization.
- Chance to find key decrease exponentially when number of block increase
- this technics where known by DES designers, so DES is very resistant to this kind of attacks

Meet in the middle is try to meet in the middle of an encryption box...

= Asymetric cryptography

=== Euler

Every $n \in \mathbb{N}$ can be written like this:

$n = p_1^{e1} \cdot p_2^{e2} \cdot \cdots \cdot p_m^{em} = \prod_{i = 1}^{m}p_i^{ei}$

So $\phi(n) = \prod_{i = 1}^{m}(p_i^{ei} - p_i^{ei - 1})$

If $n = p \cdot q$, then $\phi(n) = (p - 1) \cdot (q - 1)$

Every number modulo $n$ can be taken and if we put it to power $\phi$ modulo $n$, we obtain always $1$ !!! 

$\phi$ give the number of elements in multiplicative group of $n$

Generator allow to generate all the $n$ numbers by putting this generator to power $1, 2, \cdots, n - 1$.

It's like a basis in vector space !
