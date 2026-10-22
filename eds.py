P = 23
Q = 11
A = 2
X = 5
Y = 9
K = 7
MESSAGE = "SIGNATURE"

def custom_hash(text: str) -> int:
    h = 1
    for char in text:
        h = (h * ord(char)) % (2**16)
    return h

def egcd(a, b):
    if a == 0: return b, 0, 1
    g, x, y = egcd(b % a, a)
    return g, y - (b // a) * x, x

def mod_inv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1: raise ValueError("No inverse")
    return x % m

def sign(message: str, p: int, q: int, a: int, x: int, k: int):
    h = custom_hash(message)
    if h % q == 0:
        h = 1
    
    r = pow(a, k, p)
    r1 = r % q
    if r1 == 0:
        raise ValueError("r1 = 0, choose another k")
        
    s = (x * r1 + k * h) % q
    if s == 0:
        raise ValueError("s = 0, choose another k")
        
    return r1, s, h

def verify(message: str, r1: int, s: int, p: int, q: int, a: int, y: int) -> bool:
    if not (0 < r1 < q and 0 < s < q):
        return False
        
    h = custom_hash(message)
    if h % q == 0:
        h = 1
        
    v = pow(h, q - 2, q)
    z1 = (s * v) % q
    z2 = ((q - r1) * v) % q
    
    u = (pow(a, z1, p) * pow(y, z2, p) % p) % q
    return u == r1

if __name__ == "__main__":
    print(f"Сообщение: {MESSAGE!r}")
    print(f"Параметры: p={P}, q={Q}, a={A}, x={X}, y={Y}")
    
    r1, s, h = sign(MESSAGE, P, Q, A, X, K)
    print(f"Хэш: {h}")
    print(f"Подпись: (r1, s) = ({r1}, {s})")
    
    is_valid = verify(MESSAGE, r1, s, P, Q, A, Y)
    print(f"Подпись верна: {is_valid}")
    
    modified = "SIGNATURF"
    print(f"\nИзмененное сообщение: {modified!r}")
    is_valid_mod = verify(modified, r1, s, P, Q, A, Y)
    print(f"Подпись верна для измененного: {is_valid_mod}")