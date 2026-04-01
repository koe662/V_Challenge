#!/usr/bin/env python3
import os
import sys
import time

# 生成一个简易但绝对非线性的 S-Box (基于素数域的模幂，Z3求解缓慢)
SBOX = [(pow(x, 253, 257) % 256) for x in range(256)]
SBOX[0] = 0

def hash_verify(K, P):
    """
    全密钥验证函数，防止哈希碰撞导致的伪阳性。
    K: 9 bytes, P: 2 bytes
    """
    state = [P[0], P[1], K[0], K[1]]
    for i in range(5):
        state = [SBOX[state[j] ^ K[i+2]] for j in range(4)]
        state = [state[0]^state[1], state[1]^state[2], state[2]^state[3], state[3]^state[0]]
    return state

def generate_challenge():
    K = [int.from_bytes(os.urandom(1), 'big') for _ in range(9)]
    P = [int.from_bytes(os.urandom(1), 'big') for _ in range(2)]
    
    # ==== 前向约束 (Forward Constraints) ====
    c1 = SBOX[K[0] ^ K[1]] ^ K[2] ^ K[3]
    c2 = SBOX[K[1] ^ K[2]] ^ K[3] ^ K[4]
    c3 = SBOX[K[2] ^ K[3]] ^ K[4] ^ K[5]
    c4 = SBOX[K[3] ^ K[4]] ^ K[5] ^ K[0]
    
    # ==== 后向约束 (Backward Constraints) ====
    c6 = SBOX[K[6] ^ K[7]] ^ K[8]
    c7 = K[7] ^ SBOX[K[8]]
    
    target_hash = hash_verify(K, P)
    return P, K, (c1, c2, c3, c4, c6, c7), target_hash

def main():
    print("Welcome to the Triangulating MitM Challenge!")
    print("Can you implement the SGE-improved TA to beat the timeout?")
    print("You have 15 seconds to solve 3 rounds. Z3 won't save you here.\n")
    
    start_time = time.time()
    for round_num in range(1, 4):
        P, K, C_vals, target_hash = generate_challenge()
        c1, c2, c3, c4, c6, c7 = C_vals
        
        print(f"--- Round {round_num} ---")
        print(f"P  = {P}")
        print(f"C1 to C4 = {c1, c2, c3, c4}")
        print(f"C6, C7   = {c6, c7}")
        print(f"Target Hash = {target_hash}")
        
        try:
            ans = input("Submit 9-byte Key (hex format, e.g., 001122...): ").strip()
            submitted_k = [int(ans[i:i+2], 16) for i in range(0, 18, 2)]
        except:
            print("Invalid format!")
            sys.exit(1)
            
        if submitted_k != K:
            print("Wrong key!")
            sys.exit(1)
            
        if time.time() - start_time > 15:
            print("Timeout! You are too slow. Try implementing Triangulation MitM.")
            sys.exit(1)
            
        print("Correct!\n")
        
    print("Congratulations! Here is your flag: CTF{SGE_M1tM_T4_1s_Aw3s0m3}")

if __name__ == "__main__":
    main()
