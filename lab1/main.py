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

x1 = (a + b) / 2 - delta
x2 = (a + b) / 2 + delta


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

while round(b-a, 3) > eps:
    if func(x1) > func(x2):
        a = x1
    if func(x1) < func(x2):
        b = x2
    if func(x1) == func(x2):
        a = x1
        b = x2
    x1 = (a + b) / 2 - delta
    x2 = (a + b) / 2 + delta
print(round((a + b) / 2, 3)
      )
# Метод золотого сечения


# Метод Фибоначчи


# Поиск минимума функции на прямой
# Поиск минимума функции n переменных в заданном направлении



plt.legend(loc='upper right')
plt.grid(True)
fig.savefig('visualisation.png')
