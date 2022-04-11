import sympy


class point():
    """
    Point constructor for Elliptic Curve
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)
class P521():
    """
    NIST elliptic curve -> generates a point based on RNG is messenger client.
    Used by messenger client for:
        - pulic key encryption of key material
        - creating & verifying signatures.
    """
    def __init__(self):
        self.p = 6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057151
        self.q = 6864797660130609714981900799081393217269435300143305409394463459185543183397655394245057746333217197532963996371363321113864768612440380340372808892707005449
        self.a = -3
        self.Px_str = "c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66"
        self.Py_str = "11839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650"
        self.Px  = int(self.Px_str, 16)
        self.Py = int(self.Py_str, 16)
        self.P = point(self.Px, self.Py)
        self.ephermeral = 7326361
        self.R = self.double_and_add(self.ephermeral, self.P, self.p)
        self.ephermeral_inverse = sympy.mod_inverse(self.ephermeral, self.q)

    def double_add(self, P1, P2, p):
        if P1.x == float('inf'):
            return P2
        elif P2.x == float('inf'):
            return P1
        if P1.x == P2.x and P1.y == P2.y:
            s = ((3*pow(P1.x,2) + self.a) * sympy.mod_inverse((2*P1.y), self.p))%self.p
        else:
            if P2.x == P1.x:
                return point(float('inf'),float('inf'))
            s = ((P2.y - P1.y) * sympy.mod_inverse((P2.x - P1.x), self.p))%self.p
        x3 = (pow(s,2) - P1.x - P2.x )%self.p
        y3 = (s*(P1.x - x3) - P1.y)%self.p
        return point(x3, y3)

    def double_and_add(self, d, P, n):
        d = str(bin(d))
        d = d[3:]
        T = P

        for i in d:
            T = self.double_add(T, T, n)
            if i == '1':
                T = self.double_add(T, P, n)
        return T

    def set_private_x(self, priv_x):
        self.priv_x = priv_x
        self.pub_X = self.double_and_add(priv_x, self.P, self.p)

    def create_sig(self, h_m):
        h_m  = int(h_m, 16)
        x_r = (self.priv_x*self.R.x)%self.q
        paren = h_m + x_r
        self.s = (paren * self.ephermeral_inverse)%self.q
        return self.s, self.R.x


    def verification(self, s, h_m, pub_X, r):
        h_m  = int(h_m, 16)
        w =  sympy.mod_inverse(s, self.q)
        # print("w is :\n", w)
        u1 = (w * h_m)%self.q
        # print("u1 is :\n", u1)
        u2 = (w*r)%self.q
        # print("u2 is :\n", u2)
        u1_P = self.double_and_add(u1, self.P, self.p)
        u2_X = self.double_and_add(u2, pub_X, self.p)
        V = self.double_add(u1_P, u2_X, self.p)
        # print("V is :\n", V)
        v = (V.x)%self.q
        return v == r






###########################
