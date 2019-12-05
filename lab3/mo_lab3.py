from sympy import *
from copy import deepcopy
from math import sqrt


def func(u):
    x = u[0][0]
    y = u[1][0]
    z = u[2][0]
    return 100 * (z - ((x + y) / 2) ** 2) ** 2 + (1 - x) ** 2 + (1 - y) ** 2


def hesse_matrix(u):
    xk = u[0][0]
    yk = u[1][0]
    zk = u[2][0]
    x, y, z = symbols('x y z')
    f = 100 * (z - ((x + y) / 2) ** 2) ** 2 + (1 - x) ** 2 + (1 - y) ** 2
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


def grad_f(u):
    xk = u[0][0]
    yk = u[1][0]
    zk = u[2][0]
    x, y, z = symbols('x y z')
    f = 100 * (z - ((x + y) / 2) ** 2) ** 2 + (1 - x) ** 2 + (1 - y) ** 2
    fx = f.diff(x).subs({x: xk, y: yk, z: zk})
    fy = f.diff(y).subs({x: xk, y: yk, z: zk})
    fz = f.diff(z).subs({x: xk, y: yk, z: zk})
    return [[float(fx)], [float(fy)], [float(fz)]]


def vector_subtraction(a, b):
    c = []
    for i in range(len(a)):
        c.append([a[i][0] - b[i][0]])
    return c


def abs_grad(u):
    res = 0
    grad = grad_f(u)
    for i in range(len(u)):
        res += grad[i][0] ** 2
    return sqrt(res)


def main():
    epsilon = [1e-1, 1e-4, 1e-5]
    for i in range(len(epsilon)):
        u0 = [[3], [1], [-2]]
        it = 0
        while abs_grad(u0) > epsilon[i]:
            u0 = vector_subtraction(u0, matrix_multiplication(invert(hesse_matrix(u0)), grad_f(u0)))
            it += 1
        print('Epsilon =', epsilon[i], 'Iterations:', it)
        print('x =', u0[0], 'y =', u0[1], 'z =', u0[2])
        print('Gradient modulus =', abs_grad(u0))
        print('min F(u) =', func(u0))
        print()


if __name__ == '__main__':
    main()

# ответ x = 1, y = 1, z = 1. минимум функции f(1, 1, 1) = 0
