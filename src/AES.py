from AES_table import *
from compute import *
import numpy as np


def sub_bytes(state, is_inv=False):
    result = np.zeros((4, 4))
    if is_inv:
        for i in range(4):
            for j in range(4):
                result[i][j] = inv_s_box[int(state[i][j])]
    else:
        for i in range(4):
            for j in range(4):
                result[i][j] = s_box[int(state[i][j])]
    return result


def shift(line, times, is_right=True):
    lens = len(line)
    if is_right:
        return [line[(0 - times) % lens], line[(1 - times) % lens], line[(2 - times) % lens],
                line[(3 - times) % lens]]
    else:
        return [line[(0 + times) % lens], line[(1 + times) % lens], line[(2 + times) % lens],
                line[(3 + times) % lens]]


def to_matrix(text):
    result = [[], [], [], []]
    for i in range(len(text) // 2):
        result[i % 4].append(int(text[2 * i:i * 2 + 2], 16))
    return np.array(result)


def to_text(matrix):
    result = ''
    for i in range(4):
        for j in range(4):
            result += '{:02X}'.format(int(matrix[j][i]))
    return result


def re_matrix(texts):
    result = np.zeros((4, 4))
    for i in range(4):
        str_key = '{:08X}'.format(int(texts[i]))
        for j in range(4):
            result[j][i] = int(str_key[j * 2:j * 2 + 2], 16)
    return result


def shift_row(matrix, is_inv=False):
    for i in range(1, 4):
        matrix[i] = shift(matrix[i], 4 - i, not is_inv)
    return matrix


def mix_column(matrix, is_inv=False):
    if is_inv:
        trans = np.array(
            [[0x0e, 0x0b, 0x0d, 0x09], [0x09, 0x0e, 0x0b, 0x0d], [0x0d, 0x09, 0x0e, 0x0b], [0x0b, 0x0d, 0x09, 0x0e]])
    else:
        trans = np.array([[2, 3, 1, 1], [1, 2, 3, 1],
                         [1, 1, 2, 3], [3, 1, 1, 2]])
    return matrix_mul(trans, matrix)


def xor(a, b):
    c = []
    d = []
    for i in range(4):
        tmp = ''
        for j in range(4):
            tmp += '{:02X}'.format(int(a[j][i]))
        c.append(int(tmp, 16))
    for i in range(4):
        d.append(c[i] ^ int(b[i]))
    result = re_matrix(d)
    return result


def generate_key(key):
    result = np.zeros((11, 4))
    for i in range(4):
        result[0][i] = int(key[8 * i:8 * i + 8], 16)
        # print('{:08X}'.format(int(result[0][i])), end=" ")
    pre = int(result[0][3])
    for i in range(1, 11):
        for j in range(4):
            if j == 0:
                # print()
                temp = '{:08X}'.format(pre)
                temp = temp[2:] + temp[:2]
                tmp = ''
                for k in range(4):
                    tmp += '{:02X}'.format(
                        s_box[int(temp[k * 2:k * 2 + 2], 16)])
                pre = int(tmp, 16) ^ r_con[i - 1]
            r_key = int(result[i - 1][j]) ^ pre
            result[i][j] = r_key
            pre = r_key
            # print('{:08X}'.format(r_key), end=" ")
            # print("RESULT[%d][%d]:" % (i, j) + "{:08X}".format(r_key))
    return result


def encode(plain, key):
    plain_mat = to_matrix(plain)
    round_keys = generate_key(key)
    state = xor(plain_mat, round_keys[0])
    for i in range(9):
        after_sub = sub_bytes(state)
        after_shift = shift_row(after_sub)
        after_mix = mix_column(after_shift)
        state = xor(after_mix, round_keys[i + 1])
    after_sub = sub_bytes(state)
    after_shift = shift_row(after_sub)
    cipher_mat = xor(after_shift, round_keys[10])
    result = to_text(cipher_mat)
    return result


def decode(cipher, key):
    cipher_mat = to_matrix(cipher)
    round_keys = generate_key(key)
    state = xor(cipher_mat, round_keys[-1])
    for i in range(9):
        after_shift = shift_row(state, True)
        after_sub = sub_bytes(after_shift, True)
        after_xor = xor(after_sub, round_keys[-i - 2])
        state = mix_column(after_xor, True)
    after_shift = shift_row(state, True)
    after_sub = sub_bytes(after_shift, True)
    plain_mat = xor(after_sub, round_keys[0])
    result = to_text(plain_mat)
    return result


def main():
    print("AES 加密结果：")
    print(encode('1b5e8b0f1bc78d238064826704830cdb',
          '3475bd76fa040b73f521ffcd9de93f24'))
    print("AES 解密结果：")
    print(decode('fba4ec67020f1573ed28b47d7286d298',
          '2b24424b9fed596659842a4d0b007c61'))


if __name__ == '__main__':
    main()
