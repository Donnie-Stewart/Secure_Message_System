# This is the Secure Message System Repo. (In development)

The goal is to utilize industry standard techniques to develop a secure messaging system where Alice can send Bob messages in an insecure channel such that the information sent over the channel is indecipherable to the attacker, Eve. Will highlight the procedure below and explain the main techniques incorporated such as **Hashing, Signing & Authentication, Key Ratcheting, Encryption & Decryption, and the Block Cipher Mode of Operation.**

# Architecture:

<img src="https://github.com/Donnie-Stewart/Secure_Message_System/blob/main/overall_arch.png" align="right"
      width="350" height="750">

## Block Cipher Overview:

The main two algorithms used are [P-521](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-186-draft.pdf) and [Simon 128/256](https://eprint.iacr.org/2013/404.pdf). P-521, is used as a Public Key Agreement Protocol (which will be the key used in the Simon Cipher) and for creating the respective digital signatures for Bob and Alice. Once the key is set, Simon is used for Symmetric Cryptography. The data that gets sent across the channel is partitioned into 64 bit blocks and encrypted separately, hence the name block cipher. 

## Input & Key Ratcheting:

## Hashing:

## Key agreement Protocol & Elliptic Curve:

## P-521 Signature:

## Simon Block Cipher:

## Block Cipher Mode of Operation - CTR:

## Decryption:

## Verification:

# Usage:

# Credits:
