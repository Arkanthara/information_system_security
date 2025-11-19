= Hash functions

== Properties

- compression: result is of fixed size
- easy to compute
- is keyed hash function if a key appears, else unkeyed hash function
- multiple applications
  - modification detection
  - authentification (keyed hash functions)

=== Base properties

- preimage resistance: function works only in one way
- 2nd preimage resistance/weak collision resistance: can't find another plaintext that gives the same hash ACCORDING to given plaintext and hash
- collision resistance/strong collision resistance: impossible to find 2 plaintexts that give same hash. Plaintexts are not fixed

One-way hash functions satisfy points 1 and 2.
Strong one-way hash functions satisfy points 1, 2 and 3.

== MAC (Message Authentication Codes)

- keyed hash function family
- extremely fast
- symetric key
- can be used for message authentication !
- But warning ! Don't preserve non-repudiability !
