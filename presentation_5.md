# Bad USB devices

- USB peripheral infected
- programmable microcontrolers
- electrical only usb

## USB killer

Nombreux condensateurs qui font sauter le port usb (voire la carte mère !!)

## Protocole USB

Besoin seulement du file descriptor

=> se faire passer pour clavier car le système va simplement exécuter ce qui est donné...

Caméra infectée, se fait passer pour un clavier depuis la webcam et infecte tous le système.

## Attaques

Stuxnet: détruit des centrifugeuses d'uranium au moyen de clé usb infectée.
DuQu: espionage malware avec USB propagation
Fin7: vend malicieuses clé usb à plus de 100 compagnies.... Volé des millions de carte de crédit

## Difficulté

Savoir qu'est ce qu'on va attaquer (OS), quel est le langage utilisé (QWERTZ vs QWERTY etc...), si la cible est admin, si la session est ouverte, ...

## Protection

USB whitelisting, disable unused ports, 

# Cryptocurrencies

Bitcoin != anonymity: it's public but without names...

How to desanonymise ???

heuristic: connect unchained data (like email) to blockchain data...

Chain analysis:

1. identiry a suspicious transaction/address (like darkworld)
2. explore the flow history (graphs, tags/labels)
3. trace the paths (mixers, exchanges)
4. prioritize KYC points -> real world identity

=> allow to catch manager of a black market !!!

countermeasures:
- privacy mechanisms

payment can't be publicly link to our address
Can't use 2 times same private key ???

tracing:
- network monitoring (correlate transaction with ip address)
- exchange touchpoints 
- human errors: re-use of identifiers, 
