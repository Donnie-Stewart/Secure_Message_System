import random
from sha3_512 import SHA3_512
from P521 import P521, point
from simon import Simon
import requests
from point_decompression import compress, decompression
random.seed(234)

def write_to_aws(message, name):
    f = open(name + ".txt", "w")
    f.write(message)
    f.close()
    data = {"key": name + ".txt"}
    files = {"file": open(name + ".txt", "rb")}
    r = requests.post("https://cse234.s3-us-west-1.amazonaws.com", data=data, files=files)
    return r.status_code

def read_from_aws(name):
    r = requests.get("https://cse234.s3-us-west-1.amazonaws.com/" + name+ ".txt")
    return (r.text)

#Message and system parameters

def gen_keys():
    ec = P521()
    priv = random.getrandbits(256)
    pub = ec.double_and_add(priv, ec.P, ec.p)
    return priv, pub

priv_a , pub_A = gen_keys()
priv_x , pub_X = gen_keys()
priv_b , pub_B = gen_keys()
# print(pub_A)

#key and "plain-text" for simon
def simon_input(s,r, A_prime, message, x, B):
    r = (hex(r)[2:]).zfill(132)
    s = (hex(s)[2:]).zfill(132)
    message = [hex(ord(i))[2:] for i in message]
    message = ''.join(message)
    c1 = r + s + A_prime + message                                #"plain_text" input
    # print("r,s, a+m", len(r) , len(s) , len(A_prime),len(message) )
    ec = P521()
    key = ec.double_and_add(x, B, ec.p)
    key  = (hex(key.x)[2:])
    key = key[-64:]                                     #key for simon
    return key, c1


def key_stream(key, ctr_list):
    keys = []
    for i in range(1,len(ctr_list)+1):
        S = Simon(key)
        input = (hex(i)[2:]).zfill(32)
        k = S.encrypt(input)
        keys.append(k)
    # remove the extra keystream for the MSB block
    keys[0] = keys[0][-len(ctr_list[0]):]
    return keys


def create_cipher_text(key, plain_text):
    counter_mode_input = []
    cipher = ""
    for i in range(len(plain_text), 0, -32):            #seperate into blocks (first block usually not 32)
        if i - 32 >= 0:
            counter_mode_input.append(plain_text[i-32:i])
        else:
            counter_mode_input.append(plain_text[0:i])
    counter_mode_input.reverse()
    key_list = key_stream(key, counter_mode_input)

    for i in range(len(counter_mode_input)):
        new_block = int(key_list[i],16) ^ int(counter_mode_input[i],16)
        if i > 0:
            new_block = (str(hex(new_block)[2:].zfill(32)))
        else:
            new_block = (str(hex(new_block)[2:]))
        cipher = cipher + new_block
    return cipher


def message(message, name = None, new_priv_a = None):
    #create a'
    A_prime_priv, A_prime_pub = gen_keys()
    A_prime = compress(A_prime_pub)

    # print("Aprine", len(A_prime))
    A_prime_message = A_prime + message

    #hash of the message
    h_m = SHA3_512(A_prime_message)                                 #sha3 consumes text, produces hex string

    #signature from the hash
    signer = P521()                                         #create signer module
    if new_priv_a != None:
        print("private a used:", new_priv_a)
        signer.set_private_x(new_priv_a)
    else:
        print("private a used:", priv_a)
        signer.set_private_x(priv_a)                            #set private x, to be senders private key
    print("next private a to used:", A_prime_priv)
    s, r = signer.create_sig(h_m)                           #create a signature with the above private x

    #simon
    s_key, s_plain_text = simon_input(s,r, A_prime, message, priv_x, pub_B)
    cipher = create_cipher_text(s_key, s_plain_text)

    #create x'
    X_prime = compress(pub_X)
    # print("xprine", len(X_prime))
    cipher_X = X_prime + cipher


    if name != None:
        write_to_aws(cipher_X, name)
        return "success", A_prime_priv
    else:
        return cipher_X, A_prime_priv
    # return cipher_X




def received_message(cipher_X, name = None, A_prev = None):
    if name != None:
        cipher_X = read_from_aws(name)

    # X_x = int(cipher_X[:132], 16)
    # X_y  = int(cipher_X[132:264], 16)
    # X = point(X_x, X_y)
    # pub_A = point(5033892421266940283637646867722751325203679870579223199050293288117376921105387107215304183172199254493850756038568940387656879823023489703879909300125405262, 2125372410808401599382197388749734557303454466201537070008154406889364905959957325596058639265920193452602849423374168861119435274845806351709050129285928844)
    # print("c_x", len(cipher_X))
    #recover X
    x_prime = cipher_X[:132]
    cipher_X = cipher_X[132:]
    # print("x", x_prime)
    print("Compressed X is:", x_prime)
    X = decompression(x_prime)

    #key for simon using agreed x priv b
    ec = P521()
    key = ec.double_and_add(priv_b, X, ec.p)
    k = hex(key.x)[-64:]
    print("k is:", k)
    #uncover ciphertext
    l = (len(cipher_X))
    cipher_X = create_cipher_text(k, cipher_X)
    cipher_X = cipher_X.zfill(l)

    #receive params (r,s,A', message)
    r = cipher_X[:132]          # r is first 66 bytes
    s = cipher_X[132:264]       # s is next 66 bytes
    print("r is:", r)
    print("s is:", s)
    A_prime = cipher_X[264:396]
    print("A_prime is:", A_prime)
    message = cipher_X[396:]    # message is after r and s

    #find message
    message = bytes.fromhex(str(message)).decode('utf-8')
    print("recovered message decoded:\n", message)

    #check hash
    h_m = SHA3_512(A_prime + message)
    s, r = (int(s,16),int(r,16))
    verifyer = P521()

    #store A_prime for next key
    #use agreed upon A
    # A = decompression("3c5a70bdd5f01a723300e37619b7736410173209edd729a46a11a2d948cdf9146056924d29f0865e07cf5ec3f257dcdcb5dcd23917f1058993aadad8bfe39bf0f6a")
    # print("im the first A",hex(A.x),hex(A.y))
    # A = decompression(A_prime)
    if name == "donFirstMessage":
        A = pub_A
    elif A_prev != None:
        A = decompression(A_prev)
    else: #for local testing
        A = pub_A
    # A = point( int("1c5a70bdd5f01a723300e37619b7736410173209edd729a46a11a2d948cdf9146056924d29f0865e07cf5ec3f257dcdcb5dcd23917f1058993aadad8bfe39bf0f6a",16), int("182efcf99db788dcd911cb9de3cbe7ae2432672d5722891d73d78f879dfe622d987d3218a27e5bef9981bd6369f5cdcb9b45b331d1a9389f1bf668bbfa7b0aba31a", 16))
    # print("im the second A", hex(A.x),hex(A.y))
    # print("hex point", hex(A.x), hex(A.y) )
    t_f = verifyer.verification( s, h_m, A, r)        #consumes signature (s,r), hash, public X. produces t/f
    print("verification:\n", t_f)
    return A_prime

# plain_text = input("Enter a plain text message you want to send (ex: dolstewa@ucsc.edu)\n")
plain_text = ["dolstewa@ucsc.edu", "walkit talk it", "whhoooop", "drinkooo"]
a = None
a_prev = None
for p in plain_text:
    cipher_X, a = message(p, new_priv_a = a)
    print("cipher-text corresponding to message:\n", cipher_X)

    a_prev = received_message(cipher_X, A_prev = a_prev)

# names = ["donFirstMessage", "donSecondMessage", "donThirdMessage", "donFourthMessage"]
# # names = ["donMessage1", "donMessage2", "donMessage3"]
# a = None
# a_prev = None
# #surya's initial point
# # pub_A = point(int("1c5a70bdd5f01a723300e37619b7736410173209edd729a46a11a2d948cdf9146056924d29f0865e07cf5ec3f257dcdcb5dcd23917f1058993aadad8bfe39bf0f6a",16), int("182efcf99db788dcd911cb9de3cbe7ae2432672d5722891d73d78f879dfe622d987d3218a27e5bef9981bd6369f5cdcb9b45b331d1a9389f1bf668bbfa7b0aba31a",16))
# for n in names:
#     print(f"---- For the file {n} ---- \n")
#     succ, a = message("Random message " + n, n, a)
#     a_prev = received_message(None, n, a_prev)


# print("Firtst Try")
# c = message("")










###########
