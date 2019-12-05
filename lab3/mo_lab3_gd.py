from sympy import *
from math import sqrt


def func(u):
    x = u[0][0]
    y = u[1][0]
    z = u[2][0]
    return 100 * (z - ((x + y) / 2) ** 2) ** 2 + (1 - x) ** 2 + (1 - y) ** 2


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


def vector_multiplication_constant(a, const):
    for i in range(len(a)):
        a[i][0] *= const
    return a


def abs_grad(u):
    res = 0
    grad = grad_f(u)
    for i in range(len(u)):
        res += grad[i][0] ** 2
    return sqrt(res)


def abs_vec(u):
    res = 0
    for i in range(len(u)):
        res += u[i][0] ** 2
    return sqrt(res)


def norm_vector(vec_a, vec_b):
    res = 0
    for i in range(len(vec_a)):
        res += (vec_a[i][0] - vec_b[i][0]) ** 2
    return sqrt(res)


# def vec_add_const(vec_a, const):
#     for i in range(len(vec_a)):
#         vec_a[i][0] += const
#     return vec_a


# Выбор оптимального шага (не наискорейший)!!!!
def optimal_step(u0):
    x, y, z = symbols('x y z')
    f = 100 * (z - ((x + y) / 2) ** 2) ** 2 + (1 - x) ** 2 + (1 - y) ** 2
    fx = f.diff(x)
    fy = f.diff(y)
    fz = f.diff(z)

    fxx = fx.diff(x).subs({x: u0[0][0], y: u0[1][0], z: u0[2][0]})
    fyy = fy.diff(y).subs({x: u0[0][0], y: u0[1][0], z: u0[2][0]})
    fzz = fz.diff(z).subs({x: u0[0][0], y: u0[1][0], z: u0[2][0]})
    return float(3 / (fxx + fyy + fzz))


def gradient_descent(eps):
    it = 1
    alpha_res = []
    u0 = [[3], [1], [-2]]
    alpha_res.append(vector_subtraction(u0, u0))
    alpha_res.append(u0)

    while norm_vector(alpha_res[it], alpha_res[it - 1]) > eps:
        h = optimal_step(u0)
        # todo наискорейший спуск как тут делать?!
        print('h =', h)
        print('u0 =', u0)
        grad = vector_multiplication_constant(grad_f(u0), 1 / abs_grad(u0))
        u0 = vector_subtraction(u0, vector_multiplication_constant(grad, h))
        alpha_res.append(u0)
        it += 1
    print('Epsilon =', eps, 'Iterations:', it - 1)
    print('Gradient modulus =', abs_grad(u0))
    return u0


def main():
    # epsilon = [1e-1, 1e-4, 1e-5]
    epsilon = [1e-4]
    u0 = [[3], [1], [-2]]
    for i in range(len(epsilon)):
        result = gradient_descent(epsilon[i])
        print('x =', result[0], 'y =', result[1], 'z =', result[2])
        print('min F(u) =', func(result))
        print()


if __name__ == '__main__':
    main()

# ответ x = 1, y = 1, z = 1. минимум функции f(1, 1, 1) = 0
