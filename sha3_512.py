# -*- coding: utf-8 -*-
# Implementation by Gilles Van Assche, hereby denoted as "the implementer".
#
# For more information, feedback or questions, please refer to our website:
# https://keccak.team/
#
# To the extent possible under law, the implementer has waived all copyright
# and related or neighboring rights to the source code in this file.
# http://creativecommons.org/publicdomain/zero/1.0/
#https://github.com/XKCP/XKCP/blob/cf2a63166998349447539626ea08c27a44f4857e/Standalone/CompactFIPS202/Python/CompactFIPS202.py#L54
############ pre-modified code by ^^ ########################

def ROL64(a, n):
    return ((a >> (64-(n%64))) + (a << (n%64))) % (1 << 64)

#xor parity bits -- diffusion
def theta(lanes):
    C = [lanes[x][0] ^ lanes[x][1] ^ lanes[x][2] ^ lanes[x][3] ^ lanes[x][4] for x in range(5)]
    D = [C[(x+4)%5] ^ ROL64(C[(x+1)%5], 1) for x in range(5)]
    return [[lanes[x][y]^D[x] for y in range(5)] for x in range(5)]
#cyclic shifts of lanes with offets, move bits to different columns
def rho_and_pi(lanes):
    (x, y) = (1, 0)
    current = lanes[x][y]
    for t in range(24):
        (x, y) = (y, (2*x+3*y)%5)
        (current, lanes[x][y]) = (lanes[x][y], ROL64(current, (t+1)*(t+2)//2))
#nonlinear mapping function
def chi(lanes):
    for y in range(5):
        T = [lanes[x][y] for x in range(5)]
        for x in range(5):
            lanes[x][y] = T[x] ^((~T[(x+1)%5]) & T[(x+2)%5])

def KeccakF1600onLanes(lanes):
    #f-function of this hash
    R = 1
    for round in range(24):

        lanes = theta(lanes)

        rho_and_pi(lanes)

        chi(lanes)
        # ι- iota function: used to break symmetry
        for j in range(7):
            #first compute the round dependent constant
            R = ((R << 1) ^ ((R >> 7)*0x71)) % 256
            if (R & 2):
                lanes[0][0] = lanes[0][0] ^ (1 << ((1<<j)-1))
    return lanes

def load64(b):
    return sum((b[i] << (8*i)) for i in range(8))

def store64(a):
    return list((a >> (8*i)) % 256 for i in range(8))

#holds initial state/ calls the f function and uses matrix helper functions
def KeccakF1600(state):
    lanes = [[load64(state[8*(x+5*y):8*(x+5*y)+8]) for y in range(5)] for x in range(5)]
    lanes = KeccakF1600onLanes(lanes)
    state = bytearray(200)
    for x in range(5):
        for y in range(5):
            state[8*(x+5*y):8*(x+5*y)+8] = store64(lanes[x][y])
    return state

def Keccak(rate, capacity, inputBytes, delimitedSuffix, outputByteLen):
    #important initial declarations include ouput array, initial state (all 0's), input offset (which will move at the rate)
    outputBytes = bytearray()
    state = bytearray([0 for i in range(200)])
    rateInBytes = rate//8
    blockSize = 0
    inputOffset = 0

    #Sponge contructor/ left side of graph from lecture
    #Calls the f-function for each block, and new state becomes the
    #xor of the previous block.
    # === Absorb all the input blocks ===
    while(inputOffset < len(inputBytes)):
        blockSize = min(len(inputBytes)-inputOffset, rateInBytes)
        for i in range(blockSize):
            state[i] = state[i] ^ inputBytes[i+inputOffset]
        inputOffset = inputOffset + blockSize
        if (blockSize == rateInBytes):
            state = KeccakF1600(state)
            blockSize = 0
    #the last block to call the f function, there are two cases for this
    #where the block's padding requires another block, or where the last block
    #just needs to be padded regularly
    # === Do the padding and switch to the squeezing phase ===
    state[blockSize] = state[blockSize] ^ delimitedSuffix
    if (((delimitedSuffix & 0x80) != 0) and (blockSize == (rateInBytes-1))):
        state = KeccakF1600(state)
    state[rateInBytes-1] = state[rateInBytes-1] ^ 0x80
    state = KeccakF1600(state)

    #This is the squeezing phase, the left half of the graph from lecture
    #y0 is all that is required in this Implementation, thus only block needed
    blockSize = min(outputByteLen, rateInBytes)
    outputBytes = outputBytes + state[0:blockSize]
    outputByteLen = outputByteLen - blockSize

    return outputBytes


########### function to set original parameters of SHA3_512 ########

def SHA3_512(input):
    input = [int(hex(ord(i)),16) for i in input]
    rate = 576 #this is synonomous to the block size
    capacity = 1024 #determines the level of security for the scheme
    output = Keccak(rate, capacity, input, 0x06, 512//8)
    return ''.join('{:02x}'.format(x) for x in output)











####
