import matplotlib.pyplot as plt
import matplotlib as mpl
import math as m

dpi = 80
fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
mpl.rcParams.update({'font.size': 10})

plt.axis([10, 20, 0, 20])

plt.title('Function graph')
plt.xlabel('x')
plt.ylabel('f(x)')

# Вариант?
# Пример f(x) = (x-15)^2+5, x in [2, 200]


def func(x):
    return (x - 15) ** 2 + 5


def fibonacci(n):
    return m.pow((1 + m.sqrt(5))/2, n) - m.pow((1 - m.sqrt(5))/2, n) / m.sqrt(5)


# Входные значения
a = 2
b = 200
eps = 0.001
delta = eps / 2

# Определение количества знаков после запятой и точности eps
decimal = 0
epsilon = eps
while epsilon < 1:
    epsilon *= 10
    decimal += 1

# Визуализация
val_y = []
val_x = []
x0 = a
while x0 < b:
    val_y += [func(x0)]
    val_x += [x0]
    x0 += 0.1

plt.plot(val_x, val_y, color='blue', linestyle='-', label='func')

# Метод дихотомии (деления отрезка пополам)
right = b
left = a
counter = 0

while round(right - left, decimal) > eps:
    counter += 1
    x1 = (left + right) / 2 - delta
    x2 = (left + right) / 2 + delta
    if func(x1) > func(x2):
        left = x1
    if func(x1) < func(x2):
        right = x2
    if func(x1) == func(x2):
        left = x1
        right = x2

print('Dichotomy method:', round((left + right) / 2, 3))

# todo Количество итераций

iterDich = m.log((b - a) / eps, m.e) / m.log(2, m.e)

# todo counter и rule слишком разнятся
print(' Iteration in Dichotomy method.', 'rule:', round(iterDich, 1), ', counter:', counter)

# todo Метод золотого сечения. Дополнить тему с погрешностью (Неточное задание величины sqrt(5))
right = b
left = a
counter = 0
iterGold = m.log((b - a) / eps, m.e) / m.log(1.618, m.e)

while round(right - left, decimal) > eps:
    counter += 1
    x1 = left + 0.381966011 * (right - left)
    x2 = left + 0.618003399 * (right - left)
    if func(x1) > func(x2):
        left = x1
    if func(x1) < func(x2):
        right = x2
    if func(x1) == func(x2):
        left = x1
        right = x2

print('Golden ratio:', round((left + right) / 2, 3))
print(' Iteration in Golden ratio.', 'rule:', round(iterGold, 1), ', counter:', counter)

# todo Метод Фибоначчи. Отполировать, проверить
right = b
left = a
# F(n+2) > (b-a)/eps
num = int(m.ceil(m.log((m.sqrt(5) * (right - left)) / (eps * (3 + m.sqrt(5))), (1 + m.sqrt(5)) / 2)))

# x1 = left + 2 * (right - left) / (3 + m.sqrt(5))
# x2 = left + 2 * (right - left) / (1 + m.sqrt(5))

xx1 = left + fibonacci(num) * (right - left) / fibonacci(num + 2)
xx2 = left + fibonacci(num + 1) * (right - left) / fibonacci(num + 2)

for k in range(0, num):
    xx1 = left + fibonacci(num - k + 1) * (right - left) / fibonacci(num - k + 3)
    xx2 = left + fibonacci(num - k + 2) * (right - left) / fibonacci(num - k + 3)
    if func(xx1) > func(xx2):
        left = xx1
    if func(xx1) < func(xx2):
        right = xx2

print('Fibonacci method:', round((left + right) / 2, 3))
print(' Iterations in Fibonacci method:', num)

# todo Поиск минимума функции на прямой. тут первая реализация, ещё подумаю как оптимизировать код.
# todo ломается при изменении точности с 0.001 на 0.01!!!

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
        left = xk2 - h
        right = xk1 - h/2
    else:
        right = xk2 - h
        left = xk1 - h / 2
    print('Finding the minimum function on the line', '[', round(left, 3), ';', round(right, 3), ']')

# todo Поиск минимума функции n переменных в заданном направлении

plt.legend(loc='upper right')
plt.grid(True)
fig.savefig('visualisation.png')

# Вопросы: 1. как распределяются варианты? (самостоятельно)
#          2. использование примитивных библиотек? (использовать можно всё, что не реализует задачи напрямую)
#          3. время и дни защиты (гугл таблица?) (скинет)

