import math as m
from sympy import *


def func(x1, x2):
    return (1.5 - x1 * (1 - x2)) ** 2 + (2.25 - x1 * (1 - x2 ** 2)) ** 2 + (2.625 - x1 * (1 - x2 ** 3)) ** 2


def derivative_x1(x1, x2):
    return (2 * x2 - 2) * (-x1 * (1 - x2) + 1.5) + (2 * x2 ** 2 - 2) * (-x1 * (1 - x2 ** 2) + 2.25) + \
           (2 * x2 ** 3 - 2) * ( -x1 * (1 - x2 ** 3) + 2.625)


def derivative_x2(x1, x2):
    return 6 * x1 * x2 ** 2 * (-x1 * (1 - x2 ** 3) + 2.625) + 4 * x1 * x2 * (-x1 * (1 - x2 ** 2) + 2.25) + \
           2 * x1 * (-x1 * (1 - x2) + 1.5)


def g(x1, x2, alpha):
    y1 = derivative_x1(x1, x2)
    y2 = derivative_x2(x1, x2)
    return func(x1 - y1 * alpha, x2 - y2 * alpha)


def find_min_on_line(x1, x2, eps):
    delta = eps/2
    xk1 = 1  # может быть любым
    if g(x1, x2, xk1) > g(x1, x2, xk1 + delta):
        left = xk1
        right = xk1 + delta
        h = delta
    else:
        if g(x1, x2, xk1) > g(x1, x2, xk1 - delta):
            right = xk1
            left = xk1 - delta
            h = - delta
        else:
            print(xk1, 'is minimum')
            h = 0
    if h != 0:
        h *= 2
        xk2 = xk1 + h
        while g(x1, x2, xk1) > g(x1, x2, xk2):
            h *= 2
            xk1 = xk2
            xk2 += h

        if xk1 - h/2 > xk2 - h:
            left = xk2
            right = xk1 - h/2
        else:
            right = xk2
            left = xk1 - h / 2
        print('Finding the minimum function on the line', '[', left, ';', right, ']')
        borders = []
        borders += [left]
        borders += [right]
        return borders


def golden_ratio(x0, y0, a, b, eps):
    right = b
    left = a
    counter = 0
    iter_gold = m.log((b - a) / eps, m.e) / m.log(1.618, m.e)
    psi = (1 + m.sqrt(5)) / 2
    x1 = right - (right - left) / psi
    x2 = left + (right - left) / psi
    f2 = g(x0, y0, x2)
    f1 = g(x0, y0, x1)
    while right - left > eps:
        counter += 1
        if f1 > f2:
            left = x1
            x1 = x2
            x2 = left + (right - left) / psi
            f1 = f2
            f2 = g(x0, y0, x2)
        else:
            right = x2
            x2 = x1
            x1 = right - (right - left) / psi
            f2 = f1
            f1 = g(x0, y0, x1)
    gold_res = []
    gold_res += [(left + right) / 2]
    gold_res += [iter_gold]
    gold_res += [counter]
    return gold_res


def main():
    # Входные значения

    x1, x2 = symbols('x1 x2')

    print(func(x1, x2).diff(x1))
    print(func(x1, x2).diff(x2))

    x1, x2 = 5, 5

    eps = 0.0001

    der1 = derivative_x1(x1, x2)
    der2 = derivative_x2(x1, x2)

    counter = 0
    f1 = func(x1, x2)
    f0 = f1 - eps * 2

    while m.fabs(f0 - f1) > eps:
        counter += 1
        print('Частные производные:', der1, der2)
        borders = find_min_on_line(x1, x2, eps)
        res_gold = golden_ratio(x1, x2, borders[0], borders[1], eps)
        print('g(alpha) =', g(x1, x2, res_gold[0]))
        ans_alpha = res_gold[0]
        print('alpha =', ans_alpha)
        print('f(x1, x2) =', func(x1, x2))
        print('x1 =', x1, 'x2 =', x2)
        f0 = f1
        x1 -= ans_alpha * der1
        x2 -= ans_alpha * der2
        f1 = func(x1, x2)
        der1 = derivative_x1(x1, x2)
        der2 = derivative_x2(x1, x2)
        print('')

    print('Number of iterations = ', counter)


if __name__ == "__main__":
    main()


# таблицы с результатами проведенных исследований, где должны быть отражены:
    # начальное приближение x0,
    # задаваемая точность,
    # количество итераций,
    # число вычислений целевой функции,
    # найденная точка,
    # значение функции в ней,