from compute import *
import numpy as np


def to_matrix(num):
    result = np.zeros((8, 1)).astype('int')
    string = '{:08b}'.format(num)
    for i in range(7, -1, -1):
        if string[i] == '0':
            result[8-i-1] = 0
        elif string[i] == '1':
            result[8-i-1] = 1
    return result


def to_num(matrix):
    temp = ''
    for i in range(7, -1, -1):
        temp += str(matrix[i][0])
    result = int(temp, 2)
    return result


def inv_to_matrix(num):
    result = np.zeros((8, 1)).astype('int')
    string = '{:08b}'.format(num)
    for i in range(8):
        if string[i] == '0':
            result[i] = 0
        elif string[i] == '1':
            result[i] = 1
    return result


def inv_to_num(matrix):
    temp = ''
    for i in range(8):
        temp += str(matrix[i][0])
    result = int(temp, 2)
    return result


def get_sub(num):
    table = np.array([[1, 0, 0, 0, 1, 1, 1, 1], [1, 1, 0, 0, 0, 1, 1, 1], [1, 1, 1, 0, 0, 0, 1, 1], [
                     1, 1, 1, 1, 0, 0, 0, 1], [1, 1, 1, 1, 1, 0, 0, 0], [0, 1, 1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1, 1, 0], [0, 0, 0, 1, 1, 1, 1, 1]]).astype('int')
    add_on = np.array([[1], [1], [0], [0], [0], [1], [1], [0]]).astype('int')
    inv_num = inv(num)
    num_mat = to_matrix(inv_num)
    res_mat = matrix_add(matrix_mul(table, num_mat), add_on)
    result = to_num(res_mat)
    return result


def get_inv_sub(num):
    table = np.array([[0, 1, 0, 1, 0, 0, 1, 0], [0, 0, 1, 0, 1, 0, 0, 1], [1, 0, 0, 1, 0, 1, 0, 0], [0, 1, 0, 0, 1, 0, 1, 0], [
                     0, 0, 1, 0, 0, 1, 0, 1], [1, 0, 0, 1, 0, 0, 1, 0], [0, 1, 0, 0, 1, 0, 0, 1], [1, 0, 1, 0, 0, 1, 0, 0]])
    add_on = np.array([[0], [0], [0], [0], [0], [1], [0], [1]])
    num_mat = inv_to_matrix(num)
    res_mat = matrix_add(matrix_mul(table, num_mat), add_on)
    result = inv_to_num(res_mat)
    inv_num = inv(result)
    return inv_num


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
