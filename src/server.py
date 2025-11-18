#!/usr/bin/env python3
from Crypto.Util.number import *
from random import getrandbits, randint
import sympy, os, sys
import uuid

# 从文件读取 flag
def get_flag():
    try:
        with open("/flag","rb") as f:
            return f.read().strip()
    except:
        # 如果没有flag文件，生成随机UUID作为flag
        return f"flag{{{str(uuid.uuid4())}}}".encode()

FLAG = get_flag()
flag1 = FLAG[:len(FLAG)//2]
flag2 = FLAG[len(FLAG)//2:]

# 彩色 Banner（只展示一次）
print('''
\033[91m     ____    __    _   ____  __   ___   __ __   ________  ______    ______
\033[92m    / __ \  / /   / | / / / / /  |__ \ // / /  / ____/  |/  /   |  / ____/
\033[93m   / / / / / /   /  |/ / / / /   __/ ///_/ /  / / __/ /|_/ / /| | / __/   
\033[93m  / /_/ / / /___/ /|  / /_/ /   / __/   / /  / /_/ / /  / / ___ |/ /___   
\033[94m  \___\_\/_____/_/ |_/\____/   /____/  /_/   \____/_/  /_/_/  |_/_____/   
\033[0m
''')

class V_cha:
    def __init__(self):
        self.P1 = getPrime(1036)
        self.P2 = sympy.nextprime(self.P1)
        assert self.P2 - self.P1 < 1000
        self.Q1 = getPrime(512)
        self.Q2 = sympy.nextprime(self.Q1)
        self.e1 = getPrime(1024)
        self.e2 = sympy.nextprime(self.e1)
        self.N1 = self.P1 * self.P1 * self.Q1
        self.N2 = self.P2 * self.P2 * self.Q2

    def enc(self):
        return self.N1, self.N2, self.e1, self.e2

    def encrypt_flag(self):
        m1 = bytes_to_long(flag1)
        m2 = bytes_to_long(flag2)
        c1 = pow(m1, self.e1, self.N1)
        c2 = pow(m2, self.e2, self.N2)
        return c1, c2

def congruence_equation():
    """生成同余方程 c ≡ a + b (mod m) - 答错退出，答对给flag"""
    m = randint(10, 50)  # 模数 10-50
    a = randint(1, 50)   # a 1-50
    b = randint(1, 50)   # b 1-50
    
    # 计算正确的 c (取模后的结果)
    correct_c = (a + b) % m
    
    print(f"Solve the congruence equation: c ≡ {a} + {b} (mod {m})")
    print(f"What is the value of c? (0 <= c < {m})")
    sys.stdout.flush()
    
    try:
        user_answer = int(sys.stdin.readline().strip())
        if user_answer == correct_c:
            print("🎉 Correct! Here is your flag:")
            try:
                print(FLAG.decode())
            except:
                print(str(FLAG))
            return True
        else:
            print(f"❌ Wrong answer! The correct answer was {correct_c}")
            print("Goodbye!")
            exit(0)  # 答错直接退出
    except:
        print("❌ Invalid input! Goodbye!")
        exit(0)  # 输入无效直接退出

def keykey():
    x1 = getrandbits(32)
    x2 = getrandbits(32)
    print("solve this: ", x1, "+", x2, "=?")
    sys.stdout.flush()
    try:
        result = int(sys.stdin.readline())
    except:
        exit(0)
    if result != x1 + x2:
        print("wrong!")
        exit(0)
    else:
        print("ok!")

def main():
    print("welcome to V_Challenge")
    A = V_cha()
    coin = 5
    while coin > 0:
        print("\n1) verify")
        print("2) get ciphertext") 
        print("3) get N & e")
        print("4) congruence equation challenge (get flag)")
        print("5) exit")
        sys.stdout.flush()
        choose = sys.stdin.readline().strip()
        if choose == "1":
            keykey()
            coin -= 1
        elif choose == "2":
            c1, c2 = A.encrypt_flag()
            print(f"c1 = {c1}\nc2 = {c2}")
            coin -= 1
        elif choose == "3":
            N1, N2, e1, e2 = A.enc()
            print(f"N1 = {N1}\nN2 = {N2}\ne1 = {e1}\ne2 = {e2}")
            coin -= 1
        elif choose == "4":
            # 同余方程挑战 - 答错退出，答对给flag
            congruence_equation()
            break  # 无论对错都会退出，答对显示flag后退出，答错直接exit
        elif choose == "5":
            print("bye~")
            break
        else:
            print("wrong input")
        sys.stdout.flush()
    
    print("Game Over!")

if __name__ == "__main__":
    main()
