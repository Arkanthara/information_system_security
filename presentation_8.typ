= Adversarial attacks

Modify data in such a way the ML will answer differently...

For instance, detection can undetect some patterns... (So print this pattern on T-shirt make you invisible for IA)

== Attack types:

- black box: attacker can't see how model works.
- white box: attacker can see how model works.

== Evasion attacks

Most famous attack on ML: attacker makes small modifications on input to falsifies the output.
For instance: add some specific noise on dog image that become detected as cat.

Idea: instead of minimise gradient, attacker try to maximise it !

== Poisoning attacks

change training data of the model, that make it modified... (Ex: black dogs are predicted as cats...)

== Defense

No defense is perfect !

- Adversarial training: incorporate adversarial examples into training dataset 
- gradient masking: hide gradient sign to avoid attack on gradient maximisation
- certified robustness: learn model with a "bulle" of modifications (potentially by adversarial...)

= Multi-factor authentication

Authentication: check identity (can be cracked with brute-force)

Multi-factor authentication: use multiple authentication !

== One time password

Shared secret between phone and server.
Then, one-time password with 6 number generated.

== HMAC-based One Time Password

HMAC from key and counter. Then result is truncated to have output of right size (6 digits...)
