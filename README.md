# This is the Secure Message System Repo. (In development)

The goal is to utilize industry standard techniques to develop a secure messaging system where Alice can send Bob messages in an insecure channel such that the information sent over the channel is indecipherable to the attacker, Eve. Will highlight the procedure below and explain the main techniques incorporated such as **Hashing, Signing & Authentication, Key Ratcheting, Encryption & Decryption, and the Block Cipher Mode of Operation.**

# Architecture:

<img src="https://github.com/Donnie-Stewart/Secure_Message_System/blob/main/overall_arch.png" align="right"
      width="350" height="750">

## Block Cipher Overview:

The main two algorithms used are [P-521](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-186-draft.pdf) and [Simon 128/256](https://eprint.iacr.org/2013/404.pdf). P-521, is used as a Public Key Agreement Protocol (which will be the key used in the Simon Cipher) and for creating the respective digital signatures for Bob and Alice. Once the key is set, Simon is used for Symmetric Cryptography. The data that gets sent across the channel is partitioned into 64 bit blocks and encrypted separately, hence the name block cipher.

## Initialization:

Public Key material is generated and exchanged between Alice and Bob. First, they both agree on the Elliptic Curve they will be using (in this case, the suggested NIST curve) and then compute their unique point. P is the initial point of the curve and key material is derived using double and add s.t. aP = A, bP = B, and xP = X. In this setup, a and b correspond to Alice and Bob's private key material and x is an ephemeral used by the message sender to create the encryption Key.
- The message sender will also create an a'P = A' which is the next key to be used in decryption. Embedding the successive key material in the message is an example of the Key ratcheting procedure to continuously introduce unique key material.

## Hashing:

The first stage of the crypto-system is to produce the hash of the successive key material and message s.t. when Alice is sending Bob a message she will take the SHA3_Hash_Function( A' + message) = SHA3_Hash<sub>a</sub> . The hash of the input is a fixed size (512b) which is fast to take a digital signature of. Verifying the signature of a hashed message ensures the original message is untampered.

## P-521 Signature:

The second stage is to create a digital signature of the payload. Input is the SHA3 hash of the new key material and message s.t. P-521(SHA3_Hash<sub>a</sub>) = r, s . These values r and s are the values that represent Alice's digital signature.
- The signature, and the original A' and message (not the hash) is the input for encryption.

## Key agreement Protocol & Elliptic Curve:

To encrypt and decrypt Alice and Bob need to agree on a Key through the insecure channel. Utilizing the one-way nature of Elliptic Curve point multiplication, they can agree on the same key without an attacker, Eve, obtaining the key material.
- Alice creates a temporary public key X = xP. She uses the private x and Bob's public B to compute the Key material. Bob uses his private b and Public X to obtain the same key. As long as neither b or x is sent to the channel, Eve cannot compute the agreed key: k.
- Alice: xB = (xbP) = k
- Bob:   bX = (bxP) = k

## Simon Block Cipher:

This cipher is apart of the family of lightweight block ciphers created by the NSA. This algorithm has been rigorously tested and is considered to be secure.
The key

## Block Cipher Mode of Operation - CTR:

## Decryption:

## Verification:

# Usage:
<img src="https://github.com/Donnie-Stewart/Secure_Message_System/blob/main/first_msg.png" align="center"
      width="700" height="500">

# Credits:
