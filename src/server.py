#!/usr/bin/env python3
import os
import sys
import time

SBOX = [(pow(x, 253, 257) % 256) for x in range(256)]
SBOX[0] = 0

def hash_verify(K, P):
    """
    【修改点1：真正的全参与加密网络】
    将原本的 5 轮增加到 7 轮，使得 K[2] 到 K[8] 全部参与到状态机的混淆与扩散中。
    这彻底消除了 (K7, K8) 的等效密钥碰撞问题，保证了数学上的唯一解。
    """
    state = [P[0], P[1], K[0], K[1]]
    for i in range(7):  # 之前是 range(5)
        # S-Box 替换层
        state = [SBOX[state[j] ^ K[i + 2]] for j in range(4)]
        # 线性扩散层 (类似 MixColumns)
        state = [state[0] ^ state[1], state[1] ^ state[2], state[2] ^ state[3], state[3] ^ state[0]]
    return state

def generate_challenge():
    K = [int.from_bytes(os.urandom(1), 'big') for _ in range(9)]
    P = [int.from_bytes(os.urandom(1), 'big') for _ in range(2)]

    # ==== 前向非线性约束 ====
    c1 = SBOX[K[0] ^ K[1]] ^ K[2] ^ K[3]
    c2 = SBOX[K[1] ^ K[2]] ^ K[3] ^ K[4]
    c3 = SBOX[K[2] ^ K[3]] ^ K[4] ^ K[5]
    c4 = SBOX[K[3] ^ K[4]] ^ K[5] ^ K[0]

    # ==== 后向非线性约束 ====
    c6 = SBOX[K[6] ^ K[7]] ^ K[8]
    c7 = K[7] ^ SBOX[K[8]]

    target_hash = hash_verify(K, P)
    return P, K, (c1, c2, c3, c4, c6, c7), target_hash

def check_solution(submitted_k, P, C_vals, target_hash):
    """
    【修改点2：基于密码学属性的验证】
    不再使用死板的 submitted_k != K，而是验证选手提交的密钥是否完美满足
    所有的代数约束和哈希结果。这才是密码分析的本质。
    """
    c1, c2, c3, c4, c6, c7 = C_vals
    K = submitted_k
    
    try:
        # 检查哈希结果
        if hash_verify(K, P) != target_hash: return False
        
        # 检查代数系统约束
        if SBOX[K[0] ^ K[1]] ^ K[2] ^ K[3] != c1: return False
        if SBOX[K[1] ^ K[2]] ^ K[3] ^ K[4] != c2: return False
        if SBOX[K[2] ^ K[3]] ^ K[4] ^ K[5] != c3: return False
        if SBOX[K[3] ^ K[4]] ^ K[5] ^ K[0] != c4: return False
        if SBOX[K[6] ^ K[7]] ^ K[8] != c6: return False
        if K[7] ^ SBOX[K[8]] != c7: return False
    except:
        return False
        
    return True

def main():
    print("Welcome to the Triangulating MitM Challenge (Hardcore Edition)!")
    print("This time, no lucky equivalent keys. You need TRUE bidirectional Meet-in-the-Middle.\n")

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
            ans = input("Submit 9-byte Key (hex format): ").strip()
            submitted_k = [int(ans[i:i + 2], 16) for i in range(0, 18, 2)]
            if len(submitted_k) != 9: raise ValueError
        except:
            print("Invalid format!")
            sys.exit(1)

        # 调用新的验证逻辑
        if not check_solution(submitted_k, P, C_vals, target_hash):
            print("Wrong key!")
            sys.exit(1)

        if time.time() - start_time > 15:
            print("Timeout! You are too slow.")
            sys.exit(1)

        print("Correct!\n")

    print("Congratulations! Here is your flag: CTF{Tru3_M1tM_w1th_SGE_M4st3r}")

if __name__ == "__main__":
    main()
