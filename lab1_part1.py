import matplotlib.pyplot as plt
import matplotlib as mpl

dpi = 80
fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
mpl.rcParams.update({'font.size': 10})

plt.axis([10, 20, 0, 20])

plt.title('Function graph')
plt.xlabel('x')
plt.ylabel('f(x)')

# Вариант?
# Пример f(x) = (x-15)^2+5, x in [2, 200]

# Метод дихотомии (деления отрезка пополам)

a = 2
b = 200
eps = 0.001
delta = eps / 2


def func(x):
    return (x - 15) ** 2 + 5


val_y = []
val_x = []
x0 = a
while x0 < b:
    val_y += [func(x0)]
    val_x += [x0]
    x0 += 0.1

plt.plot(val_x, val_y, color='blue', linestyle='-', label='func')

right = b
left = a

while round(right - left, 3) > eps:
    x1 = (left + right) / 2 - delta
    x2 = (left + right) / 2 + delta
    if func(x1) > func(x2):
        left = x1
    if func(x1) < func(x2):
        right = x2
    if func(x1) == func(x2):
        left = x1
        right = x2

print('Dichotomy method: ', round((left + right) / 2, 3))

# todo Метод золотого сечения. Дополнить тему с погрешностью
right = b
left = a

while round(right - left, 3) > eps:
    x1 = left + 0.381966011 * (right - left)
    x2 = left + 0.618003399 * (right - left)
    if func(x1) > func(x2):
        left = x1
    if func(x1) < func(x2):
        right = x2
    if func(x1) == func(x2):
        left = x1
        right = x2
print('Golden ratio: ', round((left + right) / 2, 3))

# todo Метод Фибоначчи
# todo Поиск минимума функции на прямой
# todo Поиск минимума функции n переменных в заданном направлении


plt.legend(loc='upper right')
plt.grid(True)
fig.savefig('visualisation.png')

# Вопросы: 1. как распределяются варианты? (самостоятельно)
#          2. использование примитивных библиотек? (использовать можно всё, что не реализует задачи напрямую)
#          3. время и дни защиты (гугл таблица?) (скинет)

