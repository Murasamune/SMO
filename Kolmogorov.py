# Скрипцов Дмитрий, Татарченкова Анна, Поправко Ксения. Группа 19.М02
# Выполнила Татарченкова Анна

import matplotlib.pyplot as plt

L = 2  # лямбда
M = 1  # мю

n = 5  # количество каналов

h = 0.01  # шаг
T = 1000  # количество шагов

Pi_values = [[0]*T for i in range(n+1)]  # матрица вероятностей [n+1]x[T]
Pi_values[0][0] = 1  # в начальный момент времени вероятность состояния 0 равна 1
T_1 = []  # для метода Рунге-Кутты
T_2 = []  #
T_3 = []  #
T_4 = []  #


# производная вероятности (индекс, момент времени, 3 переменных для метода Рунге-Кутты)
def Pi_derivative(i, t, RK4_ratio1, RK4_ratio2, RK4_ratio3):
    if i == 0:
        return n*M*(Pi_values[1][t]+RK4_ratio2) - L*(Pi_values[0][t]+RK4_ratio1)
    elif i == n:
        return L*(Pi_values[n-1][t]+RK4_ratio2) - n*M*(Pi_values[n][t]+RK4_ratio3)
    else:
        return L*(Pi_values[i-1][t]+RK4_ratio1) - (L+n*M)*(Pi_values[i][t]+RK4_ratio2) + n*M*(Pi_values[i+1][t]+RK4_ratio3)


# метод Рунге-Кутты четвертого порядка
def RungeKutta4():
    for t in range(T-1):
        for i in range(n+1):
            T_1.append(h * Pi_derivative(i, t, 0, 0, 0))

        for i in range(n+1):
            if i == 0:
                T_2.append(h * Pi_derivative(i, t, T_1[0]/2, T_1[1]/2, 0))
            elif i == n:
                T_2.append(h * Pi_derivative(i, t, 0, T_1[n-1]/2, T_1[n]/2))
            else:
                T_2.append(h * Pi_derivative(i, t, T_1[i-1]/2, T_1[i]/2, T_1[i+1]/2))

        for i in range(n+1):
            if i == 0:
                T_3.append(h * Pi_derivative(i, t, T_2[0]/2, T_2[1]/2, 0))
            elif i == n:
                T_3.append(h * Pi_derivative(i, t, 0, T_2[n-1]/2, T_2[n]/2))
            else:
                T_3.append(h * Pi_derivative(i, t, T_2[i-1]/2, T_2[i]/2, T_2[i+1]/2))

        for i in range(n+1):
            if i == 0:
                T_4.append(h * Pi_derivative(i, t, T_3[0], T_3[1], 0))
            elif i == n:
                T_4.append(h * Pi_derivative(i, t, 0, T_3[n-1], T_3[n]))
            else:
                T_4.append(h * Pi_derivative(i, t, T_3[i-1], T_3[i], T_3[i+1]))

        for i in range(n+1):
            Pi_values[i][t+1] = Pi_values[i][t] + (T_1[i] + 2 * T_2[i] + 2 * T_3[i] + T_4[i]) / 6

        T_1.clear()
        T_2.clear()
        T_3.clear()
        T_4.clear()


# функция для построения графика
def lineplot(x_label="t", y_label="p", title="RungeKutta4"):
    x_axis = []
    for i in range(T):
        x_axis.append(h * i)

    fig = plt.figure()
    ax = fig.add_subplot()
    for i in range(n+1):
        ax.plot(x_axis, Pi_values[i], label='Состояние ' + str(i))

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)


RungeKutta4()
lineplot()

grid = plt.grid(True)
plt.legend()
plt.show()

ro = L/(n*M)
Q = (1-ro**n)/(1-ro**(n+1))
print('Приведенная интенсивность потока заявок: ' + str(ro))
print('Относительная пропускная способность: ' + str(Q))
print('Абсолютная пропускная способность: ' + str(L*Q))
print('Вероятность отказа: ' + str((ro**n)*(1-ro)/(1-ro**(n+1))))
print('Среднее число занятых каналов: ' + str(L*Q/M))
print('Среднее время прибывания заявки в СМО: ' + str(1/(n*M)))
