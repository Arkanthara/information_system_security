# XSS vulnerability

## Reflected XSS

attack on website ... script at the back of legitimate web's URL and sends it to a user (email, ...)

=> user don't see anything, but malicious script run in background !!

copy user informations / cookies etc...

## Stored XSS (/persistent XSS)

application receives data from untrusted source and remains in the web's database

## DOM-based XSS

if web application writes data to the Document object model without proper sanitiazion

## British airways

380000 booking transactions affected...

hacker Magecart steal credit card informations from usecured payment pages on popular websites...Stored XSS because all customers who accessed compromised page have been affected...

## Fortnite

## Ebay

## Prevent

- firewall
- content security policy
- cookie measurement

# Dangling pointers

Pointers on memory in C
Access to unauthorised memory !!!

Diablo III game => ability to execute code on all connected machines using dangling pointers !!!

=> set pointers to null
=> use safe languages (C++, Rust, ...)
=> correctly set flags 

# Role of explainable AI in cibersecurity threat detection

Problem: AI -> blackbox

inability to validate alerts
false positive overload
lack of actionable ??
??

problem:
automated security decisions
cannot justify security actions

XAI techniques:

transform opaque AI decitions into transparent
local / global explanations

local: particular on 1 event
global: ??

enhanced model security

benefits: improved collaboration 
XAI translate technical security into managment way (for instance) that facilitate communication...

=> XAI : transparent and trustworthy -> 
