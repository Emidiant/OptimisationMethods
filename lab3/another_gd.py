import random
import time
import math
from sympy import *


def get_f():
    x, y, z = symbols('x y z')
    func = 100 * (z - ((x + y) / 2) ** 2) ** 2 + (1 - x) ** 2 + (1 - y) ** 2
    return x, y, z, func


def f(u):
    x, y, z, func = get_f()
    return func.subs({x: u[0], y: u[1], z: u[2]})


def g(u, s, lam):
    return f([u[i] + lam * s[i] for i in range(len(u))])


def grad_f(u):
    x, y, z, func = get_f()
    fx = func.diff(x).subs({x: u[0], y: u[1], z: u[2]})
    fy = func.diff(y).subs({x: u[0], y: u[1], z: u[2]})
    fz = func.diff(z).subs({x: u[0], y: u[1], z: u[2]})

    len = math.sqrt(fx ** 2 + fy ** 2 + fz ** 2)

    return [float(fx), float(fy), float(fz)]

def grad2_f(u):
    fx = x, y, z, func = get_f()

    f_xx = func.diff(x).diff(x).subs({x: u[0], y: u[1], z: u[2]})
    f_xy = func.diff(x).diff(y).subs({x: u[0], y: u[1], z: u[2]})
    f_xz = func.diff(x).diff(z).subs({x: u[0], y: u[1], z: u[2]})
    f_yy = func.diff(y).diff(y).subs({x: u[0], y: u[1], z: u[2]})
    f_yz = func.diff(y).diff(z).subs({x: u[0], y: u[1], z: u[2]})
    f_zz = func.diff(z).diff(z).subs({x: u[0], y: u[1], z: u[2]})

    return [[f_xx, f_xy, f_xz],
            [f_xy, f_yy, f_yz],
            [f_xz, f_yz, f_zz]]

def len_vec(u):
    return math.sqrt(sum(u[i] ** 2 for i in range(len(u))))

def compulate_lam(u):
    grad1 = grad_f(u)
    len_grad = len_vec(grad1)
    if len_grad == 0:
        len_grad = 1
    s = [-grad1[i] / len_grad for i in range(len(grad1))]
    grad2 = grad2_f(u)
    lam = -sum([grad1[i] * s[i] for i in range(len(grad1))])
    denom = 0
    for i in range(len(grad1)):
        sxgrad2 = 0
        for j in range(len(grad1)):
            sxgrad2 += s[i] * grad2[i][j]
        denom += sxgrad2 * s[i]
    if denom == 0:
        return lam
    else:
        return lam / denom


def min_on_line(u, s, eps):
    delta = eps / 2
    lam = 1
    a = lam
    b = lam

    g0 = g(u, s, lam - delta)
    g1 = g(u, s, lam)
    g2 = g(u, s, lam + delta)

    if g1 > g2:
        h = delta
    elif g1 > g0:
        h = -delta
    else:
        return "min in %s" % lam

    h *= 2
    lam_next = lam + h
    g1, g2 = g(u, s, lam), g(u, s, lam_next)
    while g1 > g2:
        h *= 2
        lam = lam_next
        lam_next += h
        g1, g2 = g2, g(u, s, lam_next)

    if lam - h / 2 > lam_next - h:
        return lam_next, lam - h / 2
    else:
        return lam - h / 2, lam_next


def golden_ratio(a, b, u, s, eps):
    iterations = 0
    lam1 = a + (3 - math.sqrt(5)) / 2 * (b - a)
    lam2 = a + (math.sqrt(5) - 1) / 2 * (b - a)
    g1 = g(u, s, lam1)
    g2 = g(u, s, lam2)
    while math.fabs(b - a) > eps:
        iterations += 1
        if g1 < g2:
            b = lam2
            lam2 = lam1
            g2 = g1
            lam1 = a + (3 - math.sqrt(5)) / 2 * (b - a)
            g1 = g(u, s, lam1)
        else:
            a = lam1
            lam1 = lam2
            g1 = g2
            lam2 = a + (math.sqrt(5) - 1) / 2 * (b - a)
            g2 = g(u, s, lam2)
    lam = (a + b) / 2
    return lam


def fastest_descent(u_cur, eps):
    print(u_cur)
    grad = grad_f(u_cur)
    len_grad = len_vec(grad)
    if len_grad == 0:
        len_grad = 1
    s = [-grad[i] / len_grad for i in range(len(grad))]
    print("Grad =", s)
    a, b = min_on_line(u_cur, s, eps)

    print("Interval (%s, %s)" % (a, b))
    lam = golden_ratio(a, b, u_cur, s, eps)
    #lam = compulate_lam(u_cur)
    print("Lambda =", lam)
    u_next = [u_cur[i] + lam * s[i] for i in range(len(u_cur))]

    print("Next u =", u_next)
    f1 = f(u_cur)
    f2 = f(u_next)
    print("f1 = %s,  f2 = %s" % (f1, f2))
    iterations = 0

    ffff = [f1, f2]
    well_counter = 0
    while math.fabs(f2 - f1) > eps:
        #print("WELL_COUNTER = %s" % well_counter)
        #if well_counter == 5:
        #    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
         #   u_next = [u_next[i] + random.triangular(-15, 15, eps) for i in range(len(u_next))]
          #  well_counter = 0
        iterations += 1
        u_cur = u_next
        f1 = f2

        grad = grad_f(u_cur)
        len_grad = len_vec(grad)
        if len_grad == 0:
            len_grad = 1
        s = [-grad[i] / len_grad for i in range(len(grad))]
        print("Grad =", s)
        a, b = min_on_line(u_cur, s, eps)
        print("Interval (%s, %s)" % (a, b))
        lam = golden_ratio(a, b, u_cur, s, eps)
        #lam = compulate_lam(u_cur)
        print("Lambda =", lam)
        print(u_cur)
        u_next = [u_cur[i] + lam * s[i] for i in range(len(u_cur))]
        print("Next u =", u_next)
        f2 = f(u_next)
        print("f1 = %s,  f2 = %s" % (f1, f2))
        print()
        #flag = false
        #for i in range(len(ffff)):
        #    if math.fabs(ffff[i] - f2) <= eps * 1000:
        #        well_counter += 1
        #        u_next = [u_next[i] + random.triangular(-1, 1, eps) for i in range(len(u_next))]
        #        #ffff.clear()
        #        flag = true
        #if flag == false:
        #    ffff.append(f2)


        #flag = 0
        #for i in range(len(u_cur)):
        #    if math.fabs(u_next[i] - u_cur[i]) / u_cur[i] < eps / 2:
        #        flag += 1
        #if flag == len(u_cur):
        #    break


    print(iterations)
    print(u_next)
    print("f =", f2)
    return u_next


def main():
    # INITIALIZATION
    u = [3, 1, -2]
    eps = 1e-3

    fastest_descent(u, eps)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
