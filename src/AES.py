from AES_table import *
from compute import *
import numpy as np


def sub_bytes(state, is_inv=False):
    '''
    Sbox变换函数
    :param state: SBOX变换字节
    :param is_inv: 用于加密(False)或解密(True)
    :return: SBOX 变换后矩阵
    '''
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
    '''
    :param line: 变换的行
    :param times: 移动几位
    :param is_right:是否右移
    :return: 行变换后的行
    '''
    lens = len(line)
    if is_right:
        return [line[(0 - times) % lens], line[(1 - times) % lens], line[(2 - times) % lens],
                line[(3 - times) % lens]]
    else:
        return [line[(0 + times) % lens], line[(1 + times) % lens], line[(2 + times) % lens],
                line[(3 + times) % lens]]


def to_matrix(text):
    '''
    将字符串转为AES所用矩阵
    :param text:写入的字符串
    :return:字节矩阵
    '''
    result = [[], [], [], []]
    for i in range(len(text) // 2):
        result[i % 4].append(int(text[2 * i:i * 2 + 2], 16))
    return np.array(result)


def to_text(matrix):
    '''
    将求得的结果矩阵转为文本
    :param matrix: 结果的矩阵
    :return:结果文本
    '''
    result = ''
    for i in range(4):
        for j in range(4):
            result += '{:02X}'.format(int(matrix[j][i]))
    return result


def re_matrix(texts):
    '''
    用于轮密钥加时从4列转回矩阵
    :param texts:需要转回矩阵的列表
    :return:重组后的矩阵
    '''
    result = np.zeros((4, 4))
    for i in range(4):
        str_key = '{:08X}'.format(int(texts[i]))
        for j in range(4):
            result[j][i] = int(str_key[j * 2:j * 2 + 2], 16)
    return result


def shift_row(matrix, is_inv=False):
    '''
    行移位函数
    :param matrix:需要行变换的矩阵
    :param is_inv:是否为解密
    :return:行变换后的矩阵
    '''
    for i in range(1, 4):
        matrix[i] = shift(matrix[i], 4 - i, not is_inv)
    return matrix


def mix_column(matrix, is_inv=False):
    '''
    列混淆函数
    :param matrix:需要列混淆的矩阵
    :param is_inv:是否为解密
    :return:列混淆后的函数
    '''
    if is_inv:
        trans = np.array(
            [[0x0e, 0x0b, 0x0d, 0x09], [0x09, 0x0e, 0x0b, 0x0d], [0x0d, 0x09, 0x0e, 0x0b], [0x0b, 0x0d, 0x09, 0x0e]])
    else:
        trans = np.array([[2, 3, 1, 1], [1, 2, 3, 1],
                         [1, 1, 2, 3], [3, 1, 1, 2]])
    return matrix_mul(trans, matrix)


def xor(a, b):
    '''
    仅用于轮密钥加的字符串异或函数
    :param a:第一个字符串
    :param b:第二个字符串
    :return:轮密钥加后的矩阵
    '''
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
    '''
    轮密钥生成函数
    :param key: 密钥文本
    :return:轮密钥序列
    '''
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
    '''
    AES 加密函数
    :param plain: 明文字符串，应为128位
    :param key: 密钥字符串，应为128位
    :return: AES-128加密后结果
    '''
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
    '''
    AES-128解密函数
    :param cipher:密文字符串，应为128位
    :param key:密钥字符串，应为128位
    :return:AES-128解密后结果
    '''
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
