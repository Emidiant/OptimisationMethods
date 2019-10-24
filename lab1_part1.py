import matplotlib.pyplot as plt
import matplotlib as mpl
import math as m
import time
start_time = time.time()

# Вариант 5


def func(x):
    return (x + 5) ** 4


def fib(n):
    return m.pow((1 + m.sqrt(5))/2, n) - m.pow((1 - m.sqrt(5))/2, n) / m.sqrt(5)


def visualisation(a, b):
    # Визуализация
    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
    mpl.rcParams.update({'font.size': 10})

    plt.axis([-10, 15, 0, 100000])

    plt.title('Function graph')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    val_y = []
    val_x = []
    x0 = a
    while x0 < b:
        val_y += [func(x0)]
        val_x += [x0]
        x0 += 0.1

    plt.plot(val_x, val_y, color='blue', linestyle='-', label='func')
    plt.legend(loc='upper right')
    plt.grid(True)
    fig.savefig('visualisation.png')


def dichotomy(a, b, eps):
    # Метод дихотомии (деления отрезка пополам)
    right = b
    left = a
    delta = eps / 2
    counter = 0

    while right - left > eps:
        counter += 1
        x1 = (left + right) / 2 - delta
        x2 = (left + right) / 2 + delta
        f1 = func(x1)
        f2 = func(x2)
        if f1 > f2:
            left = x1 + delta
        if f1 < f2:
            right = x2 - delta
    # Количество итераций
    iter_dich = m.log((b - a) / eps, m.e) / m.log(2, m.e)
    res_dich = []
    res_dich += [(left + right) / 2]
    res_dich += [iter_dich]
    res_dich += [counter]
    return res_dich


# todo Метод золотого сечения. Дополнить тему с погрешностью (Неточное задание величины sqrt(5))


def golden_ratio(a, b, eps):
    right = b
    left = a
    counter = 0
    iter_gold = m.log((b - a) / eps, m.e) / m.log(1.618, m.e)
    psi = (1 + m.sqrt(5)) / 2
    x1 = right - (right - left) / psi
    x2 = left + (right - left) / psi
    f2 = func(x2)
    f1 = func(x1)
    while right - left > eps:
        counter += 1
        if f1 > f2:
            left = x1
            x1 = x2
            x2 = left + (right - left) / psi
            f1 = f2
            f2 = func(x2)
        else:
            right = x2
            x2 = x1
            x1 = right - (right - left) / psi
            f2 = f1
            f1 = func(x1)
    gold_res = []
    gold_res += [(left + right) / 2]
    gold_res += [iter_gold]
    gold_res += [counter]
    return gold_res


def fibonacci(a, b, eps):
    right = b
    left = a
    num = int(m.ceil(m.log((2 * m.sqrt(5) * (right - left)) / (eps * (3 + m.sqrt(5))), (1 + m.sqrt(5)) / 2)))
    xx1 = left + fib(num) * (right - left) / fib(num + 2)
    xx2 = left + fib(num + 1) * (right - left) / fib(num + 2)
    f2 = func(xx2)
    f1 = func(xx1)
    for k in range(1, num + 1):
        if f1 > f2:
            left = xx1
            xx1 = xx2
            f1 = f2
            xx2 = left + fib(num - k + 2) * (right - left) / fib(num - k + 3)
            f2 = func(xx2)
        if f1 < f2:
            right = xx2
            xx2 = xx1
            f2 = f1
            xx1 = left + fib(num - k + 1) * (right - left) / fib(num - k + 3)
            f1 = func(xx1)
    result = []
    result += [(left + right) / 2]
    result += [num]
    return result


# todo Поиск минимума функции на прямой. тут первая реализация, ещё подумаю как оптимизировать код.


def find_min_on_line(eps):
    delta = eps/2
    xk1 = 1  # может быть любым
    if func(xk1) > func(xk1 + delta):
        left = xk1
        right = xk1 + delta
        h = delta
    else:
        if func(xk1) > func(xk1 - delta):
            right = xk1
            left = xk1 - delta
            h = - delta
        else:
            print(xk1, 'is minimum')
            h = 0
    if h != 0:
        h *= 2
        xk2 = xk1 + h
        while func(xk1) > func(xk2):
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


def iterations_dependence(a, b):
    eps = []
    iter_dich = []
    iter_gold = []
    iter_fib = []
    i = 0
    while i < 1:
        i += 0.001
        eps += [m.log(i, 10)]
        iter_dich += [2 * dichotomy(a, b, i)[2]]
        iter_gold += [1 + golden_ratio(a, b, i)[2]]
        iter_fib += [1 + fibonacci(a, b, i)[1]]
    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
    mpl.rcParams.update({'font.size': 10})

    plt.axis([-3, 0, 0, 32])

    plt.title('Graph of the number of calculations minimized functions')
    plt.xlabel('ln(eps)')
    plt.ylabel('Iter(ln)')

    plt.plot(eps, iter_dich, color='blue', linestyle='-', label='dich')
    plt.plot(eps, iter_gold, color='red', linestyle='-', label='gold')
    plt.plot(eps, iter_fib, color='green', linestyle='-', label='fib')
    plt.legend(loc='upper right')
    plt.grid(True)
    fig.savefig('graphMinimizedCalculations.png')


def main():
    # Входные значения
    a = -10
    b = 15
    eps = 0.001
    visualisation(a, b)
    res_dich = dichotomy(a, b, eps)
    print('Dichotomy method:', res_dich[0])
    print(' Iteration in Dichotomy method.', 'rule:', res_dich[1], ', counter:', res_dich[2], '\n')
    gold_res = golden_ratio(a, b, eps)
    print('Golden ratio:', gold_res[0])
    print(' Iteration in Golden ratio.', 'rule:', gold_res[1], ', counter:', gold_res[2], '\n')
    fib_res = fibonacci(a, b, eps)
    print('Fibonacci method:', fib_res[0])
    print(' Iterations in Fibonacci method:', fib_res[1], '\n')
    find_min_on_line(eps)
    iterations_dependence(a, b)
    print("--- %s seconds ---" % round(time.time() - start_time, 3))


if __name__ == "__main__":
    main()