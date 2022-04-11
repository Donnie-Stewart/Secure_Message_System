from P521 import point

def compress(P):
    '''
    Give point: returns hex(sign + x)
    '''
    x , y = P.x, P.y
    y_bin = (bin(P.y)[2:]).zfill(521)
    sign = y_bin[0]

    x_prime = bin(x)[2:].zfill(521)
    if sign == "0":
        x_prime = "1" + x_prime
        x_prime = hex(int(x_prime,2))[2:].zfill(132)
    else:
        x_prime = "1" + x_prime
        x_prime.zfill(528)
        x_prime = (hex(int(x_prime,2))[2:]).zfill(132)
    return x_prime



def decompression(x_prime):
    '''
    input is x_prime value, return recovered (x,y)
    '''
    moduli = 6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057151
    input = bin(int(x_prime,16))[2:].zfill(528)
    sign, x = int(input[6],2), int(input[7:],2)
    b = int("051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00", 16)
    y_square = (pow(x,3) +  (- 3*x) + b)%moduli
    y = pow(y_square, (moduli + 1) // 4, moduli)

    if sign == 0:
        return point(x,y)
    else:
         return point(x, ((-1*y)%moduli))


##############
