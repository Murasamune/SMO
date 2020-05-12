# Скрипцов Дмитрий, Татарченкова Анна, Поправко Ксения. Группа 19.М02
# Выполнил Скрипцов Дмитрий

import matplotlib.pyplot as plt
import random

L = 2  # лямбда
M = 1  # мю

n = 5  # количество каналов
T = 10  # время

runs = 50000  # количество прогонов

S = []  # матрица состояний системы [T*100]x[runs]
for i in range(T * 100):
    S.append([0] * runs)

P = []  # матрица частот [n+1]x[T*100]
for j in range(n + 1):
    P.append([0] * (T * 100))

for f in range(runs):
    list_L = []  # список моментов времени, когда появляется новая заявка
    list_M = []  # список моментов времени, когда обработка заявки окончена
    tL = 0
    tM = 0

    while tL <= T:
        tL = tL + random.expovariate(1) / L  # генерируем время появления новой заявки
        list_L.append(tL)
        tM = tL + random.expovariate(1) / (M * n)  # генерируем время, когда новая заявка была бы обработана, если бы все n каналов обрабатывали только ее
        list_M.append(tM)
        count_x = sum(x > tL for x in list_M)  # количество заявок в системе

        if count_x > n:  # если система заполнена, заявка уходит
            list_L.pop()
            list_M.pop()
        elif count_x == 1:  # если она единственная, все расчеты на данном этапе верны и окончены
            continue
        else:
            list_index_value_M = []  # список индексов заявок (элементов list_M), находящихся в системе
            index_new_tM = len(list_M) - 1  # индекс новой заявки

            # формируем список пар [индекс, момент времени ухода заявки] из заявок в системе, упорядоченный по возрастанию времени
            for x in list_M:
                if x > tL:
                    list_index_value_M.append([list_M.index(x), x])
                    list_index_value_M = sorted(list_index_value_M, key=lambda kv: kv[1])

            list_change_M = []
            list_change_M_sorted = []
            j = 1
            y = 0

            # приводим все интервалы [время появления последней заявки, время ухода заявки i]
            # к одной скорости обслуживания, меньшей из всех скоростей этих интервалов
            # в list_change_M записываем новые значения интервалов [время появления последней заявки, время ухода заявки i]
            for i in range(count_x):
                if list_index_value_M[i][0] == index_new_tM:
                    list_change_M.append((list_M[index_new_tM] - tL)
                                         * count_x)
                    y = 1
                elif i == 0 or (i == 1 and y == 1):
                    list_change_M.append((count_x / (count_x - j))
                                         * (list_M[list_index_value_M[i][0]] - tL))
                    j = j + 1
                    y = 0
                else:
                    list_change_M.append(list_change_M[i - 1 - y]
                                         + (list_M[list_index_value_M[i][0]] - list_M[list_index_value_M[i - 1 - y][0]])
                                         * count_x / (count_x - j))
                    j = j + 1
                    y = 0

                # cоздаем новый список упорядоченных пар
                # list_change_M_sorted = [индекс, измененный интервал]
                list_change_M_sorted.append([list_index_value_M[i][0], list_change_M[i]])

            # сортируем его, так как с изменением интервалов мог измениться порядок выхода заявок
            list_change_M_sorted = sorted(list_change_M_sorted, key=lambda kv: kv[1])

            # возвращаем системе разную скорость обслуживания и меняем интервалы соответствующим образом
            for i in range(1, count_x):
                cut = (list_change_M_sorted[i][1] - list_change_M_sorted[i - 1][1]) * (1 - (count_x - i) / count_x)
                list_change_M_sorted[i][1] = list_change_M_sorted[i - 1][1] \
                                             + (list_change_M_sorted[i][1] - list_change_M_sorted[i - 1][1]) \
                                             * (count_x - i) / count_x
                for j in range(i + 1, count_x):
                    list_change_M_sorted[j][1] = list_change_M_sorted[j][1] - cut

            # применяем вычисления к элементам основного списка
            for i in range(count_x):
                list_M[list_change_M_sorted[i][0]] = tL + list_change_M_sorted[i][1]

    # записываем состояния системы
    count_L = 0
    count_M = 0
    for j in range(1, T * 100):
        count_L = sum(x < j * 0.01 for x in list_L)
        count_M = sum(y < j * 0.01 for y in list_M)
        temp = count_L - count_M
        S[j][f] = temp

# частоты
for t in range(T * 100):
    for i in range(n + 1):
        P[i][t] = S[t].count(i) / runs

# функция, которая строит график
def lineplot(x_label="t", y_label="p", title="Imitation"):
    fig = plt.figure()
    ax = fig.add_subplot()
    for i in range(n + 1):
        x_axis = []
        for x in range(0, T * 100):
            x_axis.append(x * 0.01)
        ax.plot(x_axis, P[i], label='Состояние ' + str(i))
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)


lineplot()
grid1 = plt.grid(True)

plt.legend()
plt.show()
