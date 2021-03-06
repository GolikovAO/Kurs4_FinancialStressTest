# Справочник по переменным
#
# Переменные доходов/расходов (data2019, data2020) - da
# data[0] - Выручка
# data[1] - Себестоимость продаж
# data[2] - Административные, коммерческие расходы
# data[3] - Сальдо процентов по кредиту
# data[4] - Прочие доходы, расходы
# data[5] - Прочее (другие доходы-расходы)
# data[6] - Налог на прибыль
# data[7] - Чистая прибыль (убыток)
#
# Переменные баланса (balance2019, balance2020)
# balance[0] - Внеоборотные активы
# balance[1] - Запасы
# balance[2] - Дебиторская задолженность
# balance[3] - Прочие оборотные активы
# balance[4] - Ден. средства, краткоср. фин. вложения
# balance[5] - Кредиторская задолженность
# balance[6] - Прочие текущие пассивы
# balance[7] - Кредиты долгосрочные
# balance[8] - Кредиты краткосрочные
# balance[9] - Уставный капитал
# balance[10] - Нераспределенная прибыль (непокрытый убыток)
# balance[11] - Прочие статьи собственного капитала


def ReworkList(list):
    tmp = []
    for row in list:
        if (row[2] == '-') or (row[2] == '(-)') or (row[2] == '(-)2'):
            row[2] = '0'
        if (row[2][0] == '('):
            row[2] = '-' + row[2][1:len(row[2]) - 1]
        tmp.append([row[0], row[1], int(row[2].replace(' ', ''))])

    # result = [tmp[0], tmp[1], tmp[3] + tmp[4], tmp[8], tmp[9] + tmp[10],
    #           (-1) * ((tmp[0] + tmp[1] + tmp[3] + tmp[4] + tmp[8] + tmp[9] + tmp[10]) + tmp[12] - tmp[16]),
    #           tmp[12], tmp[16]]
    return tmp



def CreateDataForCalc(data2019, data2020, balance2019, balance2020):
    newd2019 = [None] * 8
    newd2020 = [None] * 8
    newb2019 = [None] * 12
    newb2020 = [None] * 12
    for row in data2019:
        if row[1] == '2110':
            newd2019[0] = row  # Выручка
        elif row[1] == '2120':
            newd2019[1] = row  # Себестоимость
        elif row[1] == '2210':
            newd2019[2] = ['Административные, коммерческие расходы', '2210 + 2220', row[2]]
        elif row[1] == '2220':
            newd2019[2][2] = newd2019[2][2] + row[2]
        elif row[1] == '2320':
            newd2019[3] = ['Сальдо процентов по кредиту', '2320 + 2330', row[2]]
        elif row[1] == '2330':
            newd2019[3][2] = newd2019[3][2] + row[2]
        elif row[1] == '2340':
            newd2019[4] = ['Прочие доходы, расходы', '2340 + 2350', row[2]]
        elif row[1] == '2350':
            newd2019[4][2] = newd2019[4][2] + row[2]
        elif row[1] == '2400':
            newd2019[7] = row # Чистая прибыль(убыток)
        elif row[1] == '2410':
            newd2019[6] = row # Налог на прибыль
    newd2019[5] = ['Прочее (другие доходы-расходы)', '-', newd2019[0][2] + newd2019[1][2] + newd2019[2][2] +
                   newd2019[3][2] + newd2019[4][2] + newd2019[6][2] - newd2019[7][2]]


    for row in data2020:
        if row[1] == '2110':
            newd2020[0] = row  # Выручка
        elif row[1] == '2120':
            newd2020[1] = row  # Себестоимость
        elif row[1] == '2210':
            newd2020[2] = ['Административные, коммерческие расходы', '2210 + 2220', row[2]]
        elif row[1] == '2220':
            newd2020[2][2] = newd2020[2][2] + row[2]
        elif row[1] == '2320':
            newd2020[3] = ['Сальдо процентов по кредиту', '2320 + 2330', row[2]]
        elif row[1] == '2330':
            newd2020[3][2] = newd2020[3][2] + row[2]
        elif row[1] == '2340':
            newd2020[4] = ['Прочие доходы, расходы', '2340 + 2350', row[2]]
        elif row[1] == '2350':
            newd2020[4][2] = newd2020[4][2] + row[2]
        elif row[1] == '2400':
            newd2020[7] = row # Чистая прибыль(убыток)
        elif row[1] == '2410':
            newd2020[6] = row # Налог на прибыль
    newd2020[5] = ['Прочее (другие доходы-расходы)', '-', newd2020[0][2] + newd2020[1][2] + newd2020[2][2] +
                   newd2020[3][2] + newd2020[4][2] + newd2020[6][2] - newd2020[7][2]]


    for row in balance2019:
        if row[1] == '1100':
            newb2019[0] = ['Внеоборотные активы', row[1], row[2]]
        elif row[1] == '1210':
            newb2019[1] = row  # Запасы
        elif row[1] == '1230':
            newb2019[2] = row  # Дебиторская задолжность
        elif row[1] == '1240':
            newb2019[4] = ['Ден. средства, краткоср. фин. вложения', '1240 + 1250', row[2]]
        elif row[1] == '1250':
            newb2019[4][2] = newb2019[4][2] + row[2]
        elif row[1] == '1200':
            newb2019[3] = ['Прочие оборотные активы', '-', row[2] - (newb2019[1][2] + newb2019[2][2] + newb2019[4][2])]
        elif row[1] == '1520':
            newb2019[5] = row # Кредиторская задолжность
        elif row[1] == '1400':
            newb2019[7] = ['Кредиты долгосрочные', row[1], row[2]]
        elif row[1] == '1510':
            newb2019[8] = ['Кредиты краткосрочные', row[1], row[2]]
        elif row[1] == '1310':
            newb2019[9] = ['Уставный капитал', row[1], row[2]]
        elif row[1] == '1370':
            newb2019[10] = row # Нераспределенная прибыль (убыток)
        elif row[1] == '1500':
            newb2019[6] = ['Прочие текущие пассивы', '-', row[2]]
        elif row[1] == '1300':
            newb2019[11] = ['Прочие статьи собственного капитала', '-', row[2]]

    newb2019[6][2] = newb2019[6][2] - newb2019[8][2] - newb2019[5][2]
    newb2019[11][2] = newb2019[11][2] - newb2019[10][2] - newb2019[9][2]

    for row in balance2020:
        if row[1] == '1100':
            newb2020[0] = ['Внеоборотные активы', row[1], row[2]]
        elif row[1] == '1210':
            newb2020[1] = row  # Запасы
        elif row[1] == '1230':
            newb2020[2] = row  # Дебиторская задолжность
        elif row[1] == '1240':
            newb2020[4] = ['Ден. средства, краткоср. фин. вложения', '1240 + 1250', row[2]]
        elif row[1] == '1250':
            newb2020[4][2] = newb2020[4][2] + row[2]
        elif row[1] == '1200':
            newb2020[3] = ['Прочие оборотные активы', '-', row[2] - (newb2020[1][2] + newb2020[2][2] + newb2020[4][2])]
        elif row[1] == '1520':
            newb2020[5] = row  # Кредиторская задолжность
        elif row[1] == '1400':
            newb2020[7] = ['Кредиты долгосрочные', row[1], row[2]]
        elif row[1] == '1510':
            newb2020[8] = ['Кредиты краткосрочные', row[1], row[2]]
        elif row[1] == '1310':
            newb2020[9] = ['Уставный капитал', row[1], row[2]]
        elif row[1] == '1370':
            newb2020[10] = row  # Нераспределенная прибыль (убыток)
        elif row[1] == '1500':
            newb2020[6] = ['Прочие текущие пассивы', '-', row[2]]
        elif row[1] == '1300':
            newb2020[11] = ['Прочие статьи собственного капитала', '-', row[2]]

    newb2020[6][2] = newb2020[6][2] - newb2020[8][2] - newb2020[5][2]
    newb2020[11][2] = newb2020[11][2] - newb2020[10][2] - newb2020[9][2]

    return [newd2019, newd2020, newb2019, newb2020]