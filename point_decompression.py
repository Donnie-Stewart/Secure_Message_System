from P521 import point

def compress(P):
    '''
    Give point: returns hex(sign + x)
    '''
    x , y = P.x, P.y
    y_bin = (bin(P.y)[2:]).zfill(521)
    # sign = "0"
    sign = y_bin[0]



    x_prime = bin(x)[2:].zfill(521)
    if sign == "0":
        x_prime = "1" + x_prime
        x_prime = hex(int(x_prime,2))[2:].zfill(132)
    else:
        # print("hit")
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
    # print("input is", input)
    sign, x = int(input[6],2), int(input[7:],2)
    b = int("051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00", 16)
    y_square = (pow(x,3) +  (- 3*x) + b)%moduli
    # print("moduli",(moduli + 1) / 4)
    y = pow(y_square, (moduli + 1) // 4, moduli)
    # print("biny", bin(y))
    # print("sign", sign, type(sign))
    if sign == 0:
        return point(x,y)
    else:
         return point(x, ((-1*y)%moduli))

# x = point( int("1c5a70bdd5f01a723300e37619b7736410173209edd729a46a11a2d948cdf9146056924d29f0865e07cf5ec3f257dcdcb5dcd23917f1058993aadad8bfe39bf0f6a",16), int("182efcf99db788dcd911cb9de3cbe7ae2432672d5722891d73d78f879dfe622d987d3218a27e5bef9981bd6369f5cdcb9b45b331d1a9389f1bf668bbfa7b0aba31a", 16))
# # print(len(hex(x.y)))
# y = compress(x)
# print(y)
# # print(compress(x))
# p = decompression(y)
#
# print(hex(p.x), (hex(p.y)))
# px = 2658894132334104941120056130722138801192879152309300366960891870612888729694350077053149922651632788875087921296080324460593651686642707973027834896174907283
# py = 4220611757991424611112759208563514090385591048790930021702020218182080433966238372322708625263917014280390441041288436463216727984349010886379957251554466235
# # print(hex(px), hex(py))
# print("hex y",len(hex(py)))
# x = point(px, py)
# y = compress(x)
# print(y)
# print(decompression(y))


##############
