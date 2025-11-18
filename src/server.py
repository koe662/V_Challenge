#!/usr/bin/env python3
from random import randint
import sys
import os

def congruence_equation_challenge():
    """直接弹出同余方程挑战"""
    # 生成同余方程 c ≡ a + b (mod m)
    m = randint(10, 50)  # 模数 10-50
    a = randint(1, 50)   # a 1-50
    b = randint(1, 50)   # b 1-50
    
    # 计算正确的 c (取模后的结果)
    correct_c = (a + b) % m
    
    print("=== Congruence Equation Challenge ===")
    print(f"Solve: c ≡ {a} + {b} (mod {m})")
    print(f"Find c where 0 ≤ c < {m}")
    print("Enter your answer:")
    sys.stdout.flush()
    
    try:
        user_answer = int(sys.stdin.readline().strip())
        if user_answer == correct_c:
            print("🎉 Correct! Congratulations!")
            
            # 多种方式获取flag
            flag = None
            
            # 方法1: 从环境变量获取
            if os.environ.get('GZCTF_FLAG'):
                flag = os.environ.get('GZCTF_FLAG')
            elif os.environ.get('FLAG'):
                flag = os.environ.get('FLAG')
            # 方法2: 从文件读取
            elif os.path.exists('/flag'):
                with open("/flag", "r") as f:
                    flag = f.read().strip()
            # 方法3: 备用flag
            else:
                flag = "sdpcsec{W0w_y0u_kn01w_h0w_t00_nc_default}"
            
            print(f"Flag: {flag}")
            return True
        else:
            print(f"❌ Wrong! The correct answer was {correct_c}")
            print("Connection closed.")
            return False
    except:
        print("❌ Invalid input! Please enter a number.")
        print("Connection closed.")
        return False

def main():
    # 简洁的banner
    print("Welcome to Math Challenge!")
    print("Solve the congruence equation to get the flag!")
    print("=" * 40)
    sys.stdout.flush()
    
    # 直接开始挑战
    congruence_equation_challenge()
    
    # 无论对错都结束连接
    print("\nThank you for playing!")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
