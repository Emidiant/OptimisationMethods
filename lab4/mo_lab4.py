from numpy import arctan
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import csv
from math import sqrt

a = -2
b = 2
dpi = 80
fig = plt.figure(dpi=dpi, figsize=(700 / dpi, 500 / dpi))


def func(x):
    return arctan(x) + 1


def function_construction():
    x0 = a
    eps = 4e-3
    y_vis = []
    x_vis = []
    dataset = []
    while x0 < b - eps:
        x0 += eps
        x_vis += [x0]
        y_vis += [func(x0)]

    y_noise = []
    for i in range(len(x_vis)):
        pure = np.array(y_vis)
        noise = np.random.normal(0, 0.1, pure.shape)
        y_noise = y_vis + noise
        dataset.append([x_vis[i], y_noise[i]])

    mpl.rcParams.update({'font.size': 10})
    plt.title('Linear Regression')
    plt.ylabel('f(x)')
    plt.xlabel('x')
    plt.plot(x_vis, y_vis, color='blue', linestyle='-', label='arctg(x)+1')
    plt.plot(x_vis, y_noise, color='red', linestyle='None', marker='o', label='noise', markersize=1)
    return dataset


def create_line(alpha):
    x0 = a
    eps = 4e-3
    y_vis = []
    x_vis = []
    while x0 < b - eps:
        x0 += eps
        x_vis += [x0]
        y_vis += [alpha[0][0] * x0 + alpha[1][0]]
    plt.plot(x_vis, y_vis, color='green', linestyle='-', label='linear')
    plt.legend(loc='upper right')
    plt.grid(True)
    fig.savefig('function.png')


def create_csv(dataset):
    filename = "dataset.csv"
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(dataset)


def f_matrix_create(data):
    f = []
    for i in range(len(data)):
        t = []
        for j in range(len(data[0]) - 1):
            t.append(data[i][j])
        t.append(1)
        f.append(t)
    return f


def y_matrix_create(data):
    y = []
    for i in range(len(data)):
        y.append([data[i][len(data[0]) - 1]])
    return y


def alpha_matrix_create(data):
    alpha = []
    for i in range(len(data[0])):
        alpha.append([1])
    return alpha


def vector_addition_const(vec_a, const):
    for i in range(len(vec_a)):
        vec_a[i][0] += const
    return vec_a


def q(f, alpha, y):
    N = len(f)
    M = len(f[0])
    ans = 0
    for i in range(N):
        y_hat = 0
        for j in range(M):
            y_hat += alpha[j][0] * f[i][j]
        ans += (y_hat - y[i][0]) ** 2
    return ans / N


def vector_subtraction(vec_a, vec_b):
    c = []
    for i in range(len(vec_a)):
        c.append([vec_a[i][0] - vec_b[i][0]])
    return c


def constant_vector(vec_a, koef):
    for i in range(len(vec_a)):
        vec_a[i][0] *= koef
    return vec_a


def norm_vector(vec_a, vec_b):
    res = 0
    for i in range(len(vec_a)):
        res += (vec_a[i][0] - vec_b[i][0]) ** 2
    return sqrt(res)


def grad_q(f, alpha, y):
    N = len(f)
    M = len(f[0])
    grad = []
    for i in range(M):
        derivative = 0
        for j in range(N):
            y_hat = 0
            for k in range(M):
                y_hat += alpha[k][0] * f[j][k]
            derivative += 2 / N * f[j][i] * (y_hat - y[j][0])
        grad.append([derivative])
    return grad


def search_min(f, alpha, y):
    eps = 1e-4
    h = 0.1
    alpha_res = []
    it = 1
    alpha_1 = vector_subtraction(alpha, constant_vector(grad_q(f, alpha, y), h))
    alpha_0 = vector_addition_const(alpha_1, 1)
    alpha_res.append(alpha_0)
    alpha_1 = vector_subtraction(alpha, constant_vector(grad_q(f, alpha, y), h))
    alpha_res.append(alpha_1)
    while norm_vector(alpha_res[it], alpha_res[it - 1]) > eps:
        h = 0.1
        alpha_res.append(vector_subtraction(alpha_res[it - 1], constant_vector(grad_q(f, alpha_res[it - 1], y), h)))
        it += 1
        h /= it
    return alpha_res


def main():
    data = function_construction()
    print('Object numbers:', len(data))
    create_csv(data)
    y = y_matrix_create(data)
    f = f_matrix_create(data)
    alpha = alpha_matrix_create(data)
    result = search_min(f, alpha, y)
    alpha = []
    print('Iterations GD:', len(result))
    for i in range(len(result[0])):
        alpha.append([result[len(result) - 1][i][0]])
    print('Linear function: y =', alpha[0][0], '* x_0 +', alpha[1][0])
    create_line(alpha)
    print('MSE:', q(f, alpha, y))


if __name__ == "__main__":
    main()
