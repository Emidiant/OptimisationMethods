from sympy import *
from scipy.misc import derivative
from copy import deepcopy
from math import sqrt


def func(u):
    x = u[0][0]
    y = u[1][0]
    z = u[2][0]
    return 100 * (z - ((x + y) / 2) ** 2) ** 2 + (1 - x) ** 2 + (1 - y) ** 2


def funcd(u, d):
    h = 1e-4
    x, y, z = u[0][0], u[1][0], u[2][0]
    xd, yd, zd = d[0], d[1], d[2]
    if xd + yd + zd != 1:
        print('Wrong d, must be 1 for variable to derivative and other 0')
        return None
    result = func([[x + xd * h], [y + yd * h], [z + zd * h]]) - \
        func([[x - xd * h], [y - yd * h], [z - zd * h]])
    result /= 2 * h
    return result


def funcdd(u, d):
    h = 1e-4
    x, y, z = u[0][0], u[1][0], u[2][0]
    xd, yd, zd = d[0], d[1], d[2]
    if xd + yd + zd != 2:
        print('Wrong d, must be two 1 or one 2 (one for each variable to derivative)')
        return None
    result = func([[x + xd * h], [y + yd * h], [z + zd * h]]) + \
        func([[x - xd * h], [y - yd * h], [z - zd * h]])
    for index, i in enumerate(d):
        if i == 1:
            d[index] = -1
            break
    else:
        d = [0, 0, 0]
    xd, yd, zd = d[0], d[1], d[2]
    result -= func([[x + xd * h], [y + yd * h], [z + zd * h]]) + \
        func([[x - xd * h], [y - yd * h], [z - zd * h]])
    result /= 4 * h ** 2
    return result


def hesse_matrix(u, analytical=true):
    xk = u[0][0]
    yk = u[1][0]
    zk = u[2][0]
    x, y, z = symbols('x y z')
    f = 100 * (z - ((x + y) / 2) ** 2) ** 2 + (1 - x) ** 2 + (1 - y) ** 2
    if analytical:
        fx = f.diff(x)
        fy = f.diff(y)
        fz = f.diff(z)
        fxx = fx.diff(x).subs({x: xk, y: yk, z: zk})
        fxy = fx.diff(y).subs({x: xk, y: yk, z: zk})
        fxz = fx.diff(z).subs({x: xk, y: yk, z: zk})
        fyy = fy.diff(y).subs({x: xk, y: yk, z: zk})
        fyz = fy.diff(z).subs({x: xk, y: yk, z: zk})
        fzz = fz.diff(z).subs({x: xk, y: yk, z: zk})
        return [[fxx, fxy, fxz],
                [fxy, fyy, fyz],
                [fxz, fyz, fzz]]
    else:
        fxx = funcdd(u, [2, 0, 0])
        fxy = funcdd(u, [1, 1, 0])
        fxz = funcdd(u, [1, 0, 1])
        fyy = funcdd(u, [0, 2, 0])
        fyz = funcdd(u, [0, 1, 1])
        fzz = funcdd(u, [0, 0, 2])
        return [[fxx, fxy, fxz],
                [fxy, fyy, fyz],
                [fxz, fyz, fzz]]


def pivotize(mat_a, x):
    mat_a = deepcopy(mat_a)
    size = len(mat_a)
    row = max(range(x, size), key=lambda i: abs(mat_a[i][x]))
    if x != row:
        mat_a[x], mat_a[row] = mat_a[row], mat_a[x]
    return mat_a


# метод жордана-гаусса для поиска обратной матрицы
def invert(mat_a):
    mat_a = deepcopy(mat_a)
    n = len(mat_a)
    # Дополнить матрицу справа единичной матрицей
    for i in range(n):
        mat_a[i] += [int(i == j) for j in range(n)]
    # Прямой ход
    for x in range(n):
        mat_a = pivotize(mat_a, x)
        for i in range(x + 1, n):
            coefficient = mat_a[i][x] / mat_a[x][x]
            for j in range(x, n * 2):
                mat_a[i][j] -= coefficient * mat_a[x][j]
    # Обратный ход
    for x in reversed(range(n)):
        for i in reversed(range(x)):
            coefficient = mat_a[i][x] / mat_a[x][x]
            for j in reversed(range(n * 2)):
                mat_a[i][j] -= coefficient * mat_a[x][j]
    # Разделить строки на ведущие элементы
    for i in range(n):
        denominator = mat_a[i][i]
        for j in range(n * 2):
            mat_a[i][j] /= denominator
    # Оставить только правую часть матрицы
    for i in range(n):
        mat_a[i] = mat_a[i][n:]
    return mat_a


# перемножение матриц
def matrix_multiplication(a, b):
    n1 = len(a)
    m1 = len(a[0])
    n2 = len(b)
    m2 = len(b[0])
    res = []
    t = []
    value = 0
    if m1 == n2:
        for i in range(n1):
            for j in range(m2):
                for l in range(m1):
                    value += a[i][l] * b[l][j]
                t.append(value)
                value = 0
            res.append(t)
            t = []
    return res


def grad_f(u, analytical=True):
    xk = u[0][0]
    yk = u[1][0]
    zk = u[2][0]
    if analytical:
        x, y, z = symbols('x y z')
        f = 100 * (z - ((x + y) / 2) ** 2) ** 2 + (1 - x) ** 2 + (1 - y) ** 2
        fx = f.diff(x).subs({x: xk, y: yk, z: zk})
        fy = f.diff(y).subs({x: xk, y: yk, z: zk})
        fz = f.diff(z).subs({x: xk, y: yk, z: zk})
    else:
        fx = funcd(u, [1, 0, 0])
        fy = funcd(u, [0, 1, 0])
        fz = funcd(u, [0, 0, 1])
    return [[float(fx)], [float(fy)], [float(fz)]]


def vector_subtraction(a, b):
    c = []
    for i in range(len(a)):
        c.append([a[i][0] - b[i][0]])
    return c


def abs_grad(u,analytical=True):
    res = 0
    grad = grad_f(u,analytical)
    for i in range(len(u)):
        res += grad[i][0] ** 2
    return sqrt(res)


def main():
    epsilon = [1e-1, 1e-4, 1e-5]
    print('Analytical method')
    for i in range(len(epsilon)):
        u0 = [[3], [1], [-2]]
        it = 0
        while abs_grad(u0) > epsilon[i]:
            u0 = vector_subtraction(u0, matrix_multiplication(
                invert(hesse_matrix(u0)), grad_f(u0)))
            it += 1
        print('Epsilon =', epsilon[i], 'Iterations:', it)
        print('x =', u0[0], 'y =', u0[1], 'z =', u0[2])
        print('Gradient modulus =', abs_grad(u0))
        print('min F(u) =', func(u0))
        print()
    print('========+=============+========')
    print('Numerical method')
    for i in range(len(epsilon)):
        u0 = [[3], [1], [-2]]
        it = 0
        while abs_grad(u0,False) > epsilon[i]:
            u0 = vector_subtraction(u0, matrix_multiplication(
                invert(hesse_matrix(u0,False)), grad_f(u0,False)))
            it += 1
        print('Epsilon =', epsilon[i], 'Iterations:', it)
        print('x =', u0[0], 'y =', u0[1], 'z =', u0[2])
        print('Gradient modulus =', abs_grad(u0,False))
        print('min F(u) =', func(u0))
        print()


if __name__ == '__main__':
    main()

# ответ x = 1, y = 1, z = 1. минимум функции f(1, 1, 1) = 0
