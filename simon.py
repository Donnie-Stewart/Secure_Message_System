#simon cipher
import copy
class Simon():

    def __init__(self, key, option = "&"):

        self.rounds = 72
        self.option = option
        self.cipher_text = []
        #convert strings to lists for comparison
        self.z4 = "11010001111001101011011000100000010111000011001010010011101111"
        self.z4 = self.string_list(self.z4)
        # self.plain_text = self.hex_to_binary(plain_text)
        self.key = []
        tmp = self.hex_to_binary(key)
        #for efficient sub list creation i used:
        # https://stackoverflow.com/questions/9671224/split-a-python-list-into-other-sublists-i-e-smaller-lists
        self.key = [tmp[x-64:x] for x in range(len(tmp), 0, -64)]
        #option for simple or regular simon
        if option == "&":
            self.option = "&"
        elif option == "^":
            self.option = "^"
        self.key_expansion()

    def key_expansion(self):
        for i in range(4,72):
            tmp = self.rotate(self.key[i-1], -3)
            tmp = self.xor(tmp, self.key[i-3])
            tmp = self.xor(tmp, self.rotate(tmp,-1))
            new_key = self.xor(self.compute_inverse(self.key[i-4]), tmp)
            new_key[-1] = str(int(new_key[-1]) ^ int(self.z4[(i-4) % 62]))
            new_key[-1] = str(int(new_key[-1]) ^ 1)
            new_key[-2] = str(int(new_key[-2]) ^ 1)
            self.key.append(new_key)
            # print(i, self.list_to_hex(self.key[i]))

    def encrypt(self, cipher):
        cipher = self.hex_to_binary(cipher)
        l = len(cipher)//2
        c1 = cipher[0:l]
        c2 = cipher[l:len(cipher)]
        x = c1
        y = c2
        # self.key_expansion()
        # x = self.plain_text[0:64]
        # y = self.plain_text[64:128]
        # print(self.list_to_hex(x), self.list_to_hex(y))
        for i in range(72):
            s1,s2,s8, res, res1, res2,res3 = [],[],[], [], [],[],[]
            tmp = copy.deepcopy(x)
            if self.option == "^":
                s1 = self.rotate(x, 1)
                s8 = self.rotate(x, 8)
                res = self.xor(s1, s8 )

            elif self.option == "&":
                s1 = self.rotate(x, 1)
                s8 = self.rotate(x, 8)
                res = self.and_func(s1, s8 )

            res1 = self.xor(y, res)

            s2 = self.rotate(x,2)
            res2 = self.xor(res1, s2)
            res3 = self.xor(res2, self.key[i])

            x = copy.deepcopy(res3)
            y = copy.deepcopy(tmp)
        # print(i+1)
        # print("The cipher text is:",self.list_to_hex(x), self.list_to_hex(y))

        self.cipher_text.append(x)
        self.cipher_text.append(y)

        x , y = self.list_to_hex(x), self.list_to_hex(y)
        x = [i[2:] for i in x]
        x = ''.join(x)
        y = [i[2:] for i in y]
        y = ''.join(y)
        return x + y


    def decrypt(self, cipher):
        cipher = self.hex_to_binary(cipher)
        l = len(cipher)//2
        c1 = cipher[0:l]
        c2 = cipher[l:len(cipher)]
        x = c1
        y = c2
        # print(self.list_to_hex(x), self.list_to_hex(y))
        for i in range(72):
            s1,s2,s8, res, res1, res2,res3 = [],[],[], [], [],[],[]
            tmp = copy.deepcopy(y)
            if self.option == "^":
                s1 = self.rotate(y, 1)
                s8 = self.rotate(y, 8)
                res = self.xor(s1, s8 )

            elif self.option == "&":
                s1 = self.rotate(y, 1)
                s8 = self.rotate(y, 8)
                res = self.and_func(s1, s8 )

            res1 = self.xor(x, res)

            s2 = self.rotate(y,2)
            res2 = self.xor(res1, s2)
            res3 = self.xor(res2, self.key[71-i])

            y = copy.deepcopy(res3)
            x = copy.deepcopy(tmp)

        x , y = self.list_to_hex(x), self.list_to_hex(y)
        x = [i[2:] for i in x]
        x = ''.join(x)
        y = [i[2:] for i in y]
        y = ''.join(y)
        return x + y

        # print("The recovered Plain Text is:",self.list_to_hex(x), self.list_to_hex(y))

        # self.cipher_text.append(x)
        # self.cipher_text.append(y)

    def and_func(self, list1, list2):
        result = []
        for i in range(len(list1)):
            result.append(str(int(list1[i]) & int(list2[i])))
        return result

    def xor(self, list1, list2):
        result = []
        for i in range(len(list1)):
            result.append(str(int(list1[i]) ^ int(list2[i])))
        return result

    def rotate(self, l, n):
        list1  = copy.deepcopy(l)
        list1 = list1[n:] + list1[:n]
        #for shifting bits in the list
        #used https://stackoverflow.com/questions/2150108/efficient-way-to-rotate-a-list-in-python
        return list1
    def string_list(self, string):
        tmp = []
        tmp[:0]=string
        return tmp

    def hex_to_binary(self, string):
        h_size = len(string) * 4
        return self.string_list(str((bin(int(string, 16))[2:] ).zfill(h_size)))
    def compute_inverse(self, list1):
        list2 = []
        for i, j in enumerate(list1):
            if j == "1":
                list2.append("0")
            else:
                list2.append("1")
        return list2

    def list_to_hex(self, list1):
         temp = [list1[x:x+4] for x in range(0, len(list1), 4)]
         res = []
         for i in  temp:
            str1 = ""
            for j in i:
                str1+= j
            res.append(hex(int(str1, 2)))
         return res

# def Main():
#     # plain_text = input("Enter 128b hex plain text  (ex: 74206e69206d6f6f6d69732061207369)\n")
#     # key = input("Enter 256b hex key  (ex: 1f1e1d1c1b1a191817161514131211100f0e0d0c0b0a09080706050403020100)\n")
#     # option = input("Enter ^ for simplesimon or & for regular\n")
#     x = Simon("1f1e1d1c1b1a191817161514131211100f0e0d0c0b0a09080706050403020100")
#     print("Encrypting...")
#     c = x.encrypt("74206e69206d6f6f6d69732061207369" )
#     print("Decrypting...")
#     i = x.decrypt(c)
#     print("recovered plaintext is",i)
# Main()
