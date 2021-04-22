from compute import *
import numpy as np


def to_matrix(num):
    '''
    将数字转为单列矩阵的函数
    :param num: 需要转换的int型8位数字
    :return:一个单列矩阵
    '''
    result = np.zeros((8, 1)).astype('int')
    string = '{:08b}'.format(num)
    for i in range(7, -1, -1):
        if string[i] == '0':
            result[8-i-1] = 0
        elif string[i] == '1':
            result[8-i-1] = 1
    return result


def to_num(matrix):
    '''
    将单列矩阵（8位）转为对应数字
    :param matrix:转为数字的矩阵
    :return:对应的数字
    '''
    temp = ''
    for i in range(7, -1, -1):
        temp += str(matrix[i][0])
    result = int(temp, 2)
    return result


def inv_to_matrix(num):
    '''
    仅用于逆S盒生成中转为矩阵的函数
    :param num:转换数字，应为int型8位
    :return:对应的二进制单列矩阵
    '''
    result = np.zeros((8, 1)).astype('int')
    string = '{:08b}'.format(num)
    for i in range(8):
        if string[i] == '0':
            result[i] = 0
        elif string[i] == '1':
            result[i] = 1
    return result


def inv_to_num(matrix):
    '''
    仅用于逆S盒生成的数字转换函数
    :param matrix:转换矩阵，单列8行
    :return:对应的数字
    '''
    temp = ''
    for i in range(8):
        temp += str(matrix[i][0])
    result = int(temp, 2)
    return result


def get_sub(num):
    '''
    S盒计算
    :param num:需要计算的数字
    :return:S盒对应数字
    '''
    table = np.array([[1, 0, 0, 0, 1, 1, 1, 1], [1, 1, 0, 0, 0, 1, 1, 1], [1, 1, 1, 0, 0, 0, 1, 1], [
                     1, 1, 1, 1, 0, 0, 0, 1], [1, 1, 1, 1, 1, 0, 0, 0], [0, 1, 1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1, 1, 0], [0, 0, 0, 1, 1, 1, 1, 1]]).astype('int')
    add_on = np.array([[1], [1], [0], [0], [0], [1], [1], [0]]).astype('int')
    inv_num = inv(num)
    num_mat = to_matrix(inv_num)
    res_mat = matrix_add(matrix_mul(table, num_mat), add_on)
    result = to_num(res_mat)
    return result


def get_inv_sub(num):
    '''
    逆S盒计算
    :param num:需要计算的数字
    :return:逆S盒对应的数字
    '''
    table = np.array([[0, 1, 0, 1, 0, 0, 1, 0], [0, 0, 1, 0, 1, 0, 0, 1], [1, 0, 0, 1, 0, 1, 0, 0], [0, 1, 0, 0, 1, 0, 1, 0], [
                     0, 0, 1, 0, 0, 1, 0, 1], [1, 0, 0, 1, 0, 0, 1, 0], [0, 1, 0, 0, 1, 0, 0, 1], [1, 0, 1, 0, 0, 1, 0, 0]])
    add_on = np.array([[0], [0], [0], [0], [0], [1], [0], [1]])
    num_mat = inv_to_matrix(num)
    res_mat = matrix_add(matrix_mul(table, num_mat), add_on)
    after_mat = inv_to_num(res_mat)
    result = inv(after_mat)
    return result


def main():
    print("SBOX:")
    print('\t0\t1\t2\t3\t4\t5\t6\t7\t8\t9\tA\tB\tC\tD\tE\tF')
    for i in range(256):
        if i % 16 == 0:
            print('\n%X\t' % (i//16), end='')
        print('{:02X}'.format(get_sub(i)), end='\t')
    print("\nINV_SBOX:")
    print('\t0\t1\t2\t3\t4\t5\t6\t7\t8\t9\tA\tB\tC\tD\tE\tF')
    for i in range(256):
        if i % 16 == 0:
            print('\n%X\t' % (i//16), end='')
        print('{:02X}'.format(get_inv_sub(i)), end='\t')


if __name__ == "__main__":
    main()
