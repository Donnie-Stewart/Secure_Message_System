# This is the Secure Message System Repo

The goal is to utilize industry standard techniques to develop a secure messaging system where Alice can send Bob messages in an insecure channel such that the information sent over the channel is indecipherable to the attacker, Eve. Note that this is not something that should be used directly, but shows an implementation that encompases many cryptographic techniques and how to pair them together. Below, I also illustrate a simple attack and how this system handles it. Thus, I will highlight the procedure below and explain the main techniques incorporated such as **Hashing, Signing & Authentication, Key Ratcheting, Encryption & Decryption, and the Block Cipher Mode of Operation.** 

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

This cipher is a part of the family of lightweight block ciphers created by the NSA. This algorithm has been rigorously tested and is considered to be secure. This cipher is utilized to create the ciphertext blocks to XOR with the plaintext. Essentially, it is used to create a key stream for every block which depends on the size of the message being sent. (And this system can accept arbitrary lengths). 

## Block Cipher Mode of Operation - CTR:
To ensure a strong encryption for messages larger than one block, it is important to include a Block Cipher Mode of Operation. A detailed explaination can be found [here](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation).
Specifically in this mock messaging system I implemented CTR (short for counter) which involves XOR-ing a sequence of vectors with the plaintext and ciphertext blocks. 

## Decryption:
After parsing the encrypted output Bob will use the agreed upon key to decrypt the message. This will reveal r,s to be used in the ECDSA signature verfication. If Bob can authenticate the messages authenticity he will store Alice's next public key and display the message. 

## Verification:
Signature verification is one of many instances of Elliptic Curve Cryptography (ECC) used in this project, specially, ECDSA. Functionally, ECDSA and DSA provide the same security guarantees as they both reduce to the difficulty of solving the discrete log problem problem, yet ECDSA provides this security guarantee with far less bits. DSA requires key lengths of 3072 bits to provide 128 bits of security, ECDSA can accomplish the same with only 256-bit keys.

## Usage:
To use simply pull in and run the main file - messenger.py - as seen below. 
There is a display prompt that takes in user input to either encrypt or decrypt a message. Selecting either will require a file name to read or write from. Selecting E, will encrpt the message into a file using all the practices described above. Selecting D, will read from that file and will display the recovered message with a verifcation. If the message verification is False, then the message recovered has been tampered with. In this case, the message "Hello Bob!" is encrypted into the file "first_message.txt". Immeadiately afterwards, D(ecrypt) is selected for the file "first_message.txt". The cipher text contained in the file is then displayed and then the process of decryption follows. Once completed, the recovered message and verification. is displayed. 
<img src="https://github.com/Donnie-Stewart/Secure_Message_System/blob/main/first_msg.png" align="center"
      width="1000" height="400">
      
## Tampered File Example:
One security guarantee of this system includes determining whether files are tampered with before they are received. Below, the conversation is continued by encrypting another message "How are you?" to file "second_message". In between the completion of this command, and Decrypt, I manually went into the file and changed the last digit from a [5](https://github.com/Donnie-Stewart/Secure_Message_System/blob/main/untampered.png) to [4](https://github.com/Donnie-Stewart/Secure_Message_System/blob/main/tampered.png). As seen, this slightly currupts the recovered message and then causes the verification to fail. Verification is a vital security component when communicating over the internet. In this project, ECDSA ensures the authenticity of each message. 
<img src="https://github.com/Donnie-Stewart/Secure_Message_System/blob/main/snd_msg.png" align="center"
      width="1000" height="400">
## Credits:

All the code written is my own unless explicitly specified in the code. System archicture diagram used from Graduate Computer Science coursework at UCSC - CSE 234 "Cryptography" by [Professor Darrell Long](https://darrelllong.github.io/) and [James Hughes](https://users.soe.ucsc.edu/~japhughe/)
