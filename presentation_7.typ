= Blockchain

- Each block contains transactions
- Each block is chained to other by its HASH

== How it works

- Transactions are collected into blocks
- Block is validate by network nodes using consensus protocol
- Mined block is added to blockchain

== Consensus mechanisms

- Proof of work: solving computational challenge
- Proof of stake: 
- Proof of authority: trusted nodes validate others

Blockchain is transparent !! 

== Zero-knowledge proof (ZKP)

- Caverne d'Alibaba

=== How it works ?

- Proof must be short, don't divulgate any data, ...

== zk-SNARKs (Zero-knowledge Succinct Non-Interactive Arguments of Knowledge)

- Zero-knowledge: no private information shared
- blabla

== zk-STARK

- Scalability
- Transparent
- ARgument of Knowledge

= Buffer overflow attacks

Get access to bad memory address to run program (like handlers) or only collect data

Attack in 1988 with a program that copies itself and that slow down computer... Around 10M to 100M dollars lost.

Defense:
- code level defenses: use length for memory access... Ex: strncpy instead of strcpy...
- compile-time defenses: input validation / memory-safe languages
- compile-time defenses: random values placed between buffers and return addresses (compiler insert checks before function returns), flag correct set to stop program in stack buffer overflow
  - control-flow integrity
  - address space layout randomization
- dynamic detection:
  - runtime memory scanning
  - dynamic taint analysis (track untrusted input data through the program)

= AI Jailbraking

LLM interprets normal language as command -> use it to infect system !

Ex: hide informations in email. Then, when user try to summarise it, it will execute bad code !
Ex: ask LLM to give source code ???

=== Input control
- prompt injection pattern detection

=== Output control

=== Access control

=== Monitoring and Alerting

- security event logging
- real-time monitoring
- alert thresholds
- in

=== Architecture security and deployment

=== Testing and Validation


