= Contactless payment

== Introduction

After covid, there are more contactless payment

== Functionality

Based on NFC technology

Securities:

- bank card
- smartphone
- payment limit

== Threats

- skimming NFC
- spoil
- relay attack by repeating signal
- phishing and fake QR code

== Protection

- encryption by banks
- strong authentication (biometric, pin, Mfa)
- good practices

== Innovation

- biometric payment
- blockchain
- IA/ML for anomalies detection
- post-quantum security

= Satellite security

A lot of usage in our life

- GPS
- TV
- communication (army)

Different kind of satellites

- polar orbiting satellite
- geostationary satellite

== Satellite overview

Around 14904 satellites

Signal send to satellite, and then send from satellite.

=== Composition

- onboard computer
- sensors
- actuators (control position of satellite)
- power system
- communication system

=== Security

- confidentiality
- integrity
- availability

Communication between satellites: laser
Communication satellite-earth: send data with noise in only direction of the antenna

Jamming: send it's own signal so it replace data !

Narrowband: focused on 1 frequency
Broadband Jamming: just add noise on all frequencies

Anti-jamming
- send on multiple frequencies and reconstruct signal at the end
- blabla

=== Attacks

- send missile on satellite
- invisible energy attack: send waves that render satellite unusuable

USA, Russia, China, India

Spoofing: sending fake satellite signals to trick receivers into false positions or times

Protection: check direction of signal and distortion of signal according to dopler effect

= IoT security

== Definition

Physical device that collect and exchange data though the internet

Limited resources as memory, cpu, ...

Hackers can exploit open ports, ...

MOST IOT ATTACKS EXPLOIT WEAKNESSES IN SOFTWARE !

=== Best practices

==== Software

- secure bootloader
- updates cryptographically signed
- limit privileges
- blabla 

==== Hardware

- connection on uart/jtag to spoil data
- ...

-> debug ports must be disabled or removed before production
-> ...

=== Case study

==== Mirai

Mirai botnet: search on internet the IoT objects and try default and weak credentials

Platform like Twitter, Netflix has been impacted

- try credentials
- load binary and connect device to command and control server
- lot of devices simustaleously

==== stuxnet

Expanded by USB

Modify nuclear reactors speed and send false data to controllers

Finally, nuclear reactors were broken

=== Conclusion

Only a global proactive approach can deal with IoT security !
