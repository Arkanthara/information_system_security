padding -> message multiple of 512 !!!!!
split message in blocks of 512 bits
each block go in compression function
the output will be used as intermediate result of the next block compression function

block 512 will be considered as list of blocks of 42 bits

Proof of work

n -> sha256(n) = digest
