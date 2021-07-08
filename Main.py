from design import *
from PyQt5 import Qt
import sys
import Organization
import pulp
import pandas as pd
import os

app = QtWidgets.QApplication(sys.argv)
app.setStyle("Fusion")
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.showMaximized()


dict_rownames = ['Выручка', 'Себестоимость продаж', 'Валовая прибыль (убыток)', 'Коммерческие расходы',
                  'Управленческие расходы', 'Прибыль (убыток) от продаж', 'Доходы от участия\nв других организациях',
                  'Проценты к получению', 'Проценты к уплате', 'Прочие доходы', 'Прочие расходы', 'Прибыль (убыток)\nдо налогооблажения',
                  'Налог на прибыль', 'В т.ч. текущий налог на прибыль', 'Отложенные налог на прибыль', 'Прочее', 'Чистая прибыль (убыток)',
                  'Результат от переоценки\nвнеоборотных активов, не включаемый\nв чистую прибыль (убыток) периода',
                  'Результат от прочих операций,\nне включаемый в чистую прибыль\n(убыток) периода',
                  'Налог на прибыль от операций,\nрезультат которых не включается\nв читсую прибыль (убыток)',
                  'Совокупный финансовый результат периода']

dict_analysis = ['Выручка', 'Себестоимость\nпроданных товаров', 'Административные и\nкоммерческие расходы', 'Сальдо процентов по кредиту',
                 'Прочие доходы-расходы', 'Прочее\n(другие доходы-расходы)', 'Налог на прибыль', 'Чистая прибыль']

dict_columnnames = ['Наименование\nпоказателя', 'Значение', 'Доля от\nвыручки']

kTableValues = []
data2019 = []
data2020 = []
part2019 = []
part2020 = []
balance2019 = []
balance2020 = []
dirs = []


def ReworkList(list):
    tmp = []
    for row in list:
        if (row == '-') or (row == '(-)'):
            row = '0'
        if (row[0] == '('):
            row = '-' + row[1:len(row) - 1]
        tmp.append(int(row.replace(' ', '')))

    result = [tmp[0], tmp[1], tmp[3] + tmp[4], tmp[8], tmp[9] + tmp[10],
              (-1) * ((tmp[0] + tmp[1] + tmp[3] + tmp[4] + tmp[8] + tmp[9] + tmp[10]) + tmp[12] - tmp[16]),
              tmp[12], tmp[16]]
    return result

def CalcPart(list):
    tmp = []
    for i in range(0, 8):
        tmp.append(round(list[i] / list[0], 3))
    return tmp

def on_click():
    global part2019, part2020, data2019, data2020, balance2019, balance2020
    part2019.clear()
    part2020.clear()
    data2019.clear()
    part2020.clear()
    balance2019.clear()
    balance2020.clear()
    INN = ui.lineEdit.text()
    org = Organization.Organization(INN)
    data2019 = ReworkList(org.Get2019DataFromExcel())
    data2020 = ReworkList(org.Get2020DataFromExcel())
    part2019 = CalcPart(data2019)
    part2020 = CalcPart(data2020)
    balance2019 = org.GetBalance2019()
    balance2020 = org.GetBalance2020()
    StartBalance(balance2019, 2019)
    StartBalance(balance2020, 2020)
    org.GetNameAndAddress()
    ui.table2019.setRowCount(len(data2019))
    ui.table2019.setColumnCount(3)
    ui.table2020.setRowCount(len(data2020))
    ui.table2020.setColumnCount(3)
    ui.table_k.setRowCount(len(data2019) - 1)
    ui.table_k.setColumnCount(1)
    ui.table_k.setHorizontalHeaderLabels(['Изменение\n%'])
    #ui.table2019.setVerticalHeaderLabels(dict_rownames)
    ui.table2019.setHorizontalHeaderLabels(dict_columnnames)
    #ui.table2020.setVerticalHeaderLabels(dict_rownames)
    ui.table2020.setHorizontalHeaderLabels(dict_columnnames)
    for i in range(0, len(data2019)):
        ui.table2019.setItem(i, 0, QtWidgets.QTableWidgetItem(str(dict_analysis[i])))
        ui.table2019.setItem(i, 1, QtWidgets.QTableWidgetItem(str(data2019[i])))
        ui.table2019.setItem(i, 2, QtWidgets.QTableWidgetItem(str(round(part2019[i] * 100, 1)) + '%'))
        ui.table2020.setItem(i, 0, QtWidgets.QTableWidgetItem(str(dict_analysis[i])))
        ui.table2020.setItem(i, 1, QtWidgets.QTableWidgetItem(str(data2020[i])))
        ui.table2020.setItem(i, 2, QtWidgets.QTableWidgetItem(str(round(part2020[i] * 100, 1)) + '%'))
    ui.table2019.resizeColumnsToContents()
    ui.table2019.resizeRowsToContents()
    ui.table2020.resizeColumnsToContents()
    ui.table2020.resizeRowsToContents()
    ui.textOrgName.setText(org.Name)
    ui.textOrgAddress.setText(org.Address)
    ui.label2019.setVisible(True)
    ui.table2019.setVisible(True)
    ui.radioButton1.setVisible(True)
    ui.radioButton2.setVisible(True)
    ui.label_OrgName.setVisible(True)
    ui.textOrgName.setVisible(True)
    ui.label_OrgAddress.setVisible(True)
    ui.textOrgAddress.setVisible(True)
    ui.table_k.setVisible(True)
    ui.table_k.resizeColumnsToContents()
    ui.buttonResult.setVisible(True)
    ui.labelZLP.setVisible(True)
    ui.buttonZLP.setVisible(True)
    ui.balancetable2019.setVisible(True)
    GetCompanyList()


def radiobuttonchek():
    if (ui.radioButton1.isChecked()):
        ui.table2019.setVisible(True)
        ui.label2019.setText("Данные за 2019г")
        ui.table2020.setVisible(False)
        ui.balancetable2019.setVisible(True)
        ui.balancetable2020.setVisible(False)
    if (ui.radioButton2.isChecked()):
        ui.table2019.setVisible(False)
        ui.label2019.setText("Данные за 2020г")
        ui.table2020.setVisible(True)
        ui.balancetable2019.setVisible(False)
        ui.balancetable2020.setVisible(True)




def linProg():
    tmp = []
    ui.tableZLP.setRowCount(7)
    ui.tableZLP.setColumnCount(2)
    if (ui.radioButton1.isChecked()):
        c = data2019
        part = part2019
    if (ui.radioButton2.isChecked()):
        c = data2020
        part = part2020
    x = []
    for i in range(0, 8):
        if (i==6):
            x.append(pulp.LpVariable('x' + str(i), lowBound=1, upBound=1))
        else:
            x.append(pulp.LpVariable('x' + str(i), lowBound=0.00, upBound=2.00))
    problem = pulp.LpProblem('0', pulp.LpMinimize)
    b = c[0] * (c[7] - c[6]) / (c[1] + c[0])
    problem += c[0]*x[0] + c[1]*x[1] + c[2]*x[2] + c[3]*x[3] + c[4]*x[4] + c[5]*x[5] + c[6]*x[6], "Функция цели"
    problem += (c[0] * x[0] + c[1] * x[1] + c[2] * x[2] + c[3] * x[3] + c[4] * x[4] + c[5] * x[5] + c[6] * x[6]) >= b
    problem += c[0]*x[0] * part[1] == c[1]*x[1]
    problem += c[0] * x[0] * part[2] == c[2] * x[2]
    problem += c[0] * x[0] * part[3] == c[3] * x[3]
    problem += c[0] * x[0] * part[4] == c[4] * x[4]
    problem += c[0] * x[0] * part[5] == c[5] * x[5]
    problem.solve()
    for variable in problem.variables():
        tmp.append([variable.name, variable.varValue])

    for i in range(0, 7):
        ui.tableZLP.setItem(i, 0, QtWidgets.QTableWidgetItem(str(tmp[i][0])))
        ui.tableZLP.setItem(i, 1, QtWidgets.QTableWidgetItem(str(tmp[i][1])))

    ui.labelIdex.setVisible(True)
    ui.tableZLP.setVisible(True)
    ui.tableZLP.resizeRowsToContents()
    ui.tableZLP.resizeColumnsToContents()
    ui.labelIndexValue.setText(str(round(b, 2)))

def CalcResultTable():
    ui.tableResult.setRowCount(8)
    ui.tableResult.setColumnCount(3)
    ui.tableResult.setHorizontalHeaderLabels(dict_columnnames)
    kTableValues.clear()
    tmp = []
    for i in range(0, 8):
        if (ui.table_k.item(i, 0) == None):
            kTableValues.append(0)
        else:
            kTableValues.append(ui.table_k.item(i, 0).text())
    if (ui.radioButton1.isChecked()):
        for i in range(0, 8):
           tmp.append(round(int(ui.table2019.item(i, 1).text()) * (100 + float(kTableValues[i])) / 100, 0))
    if (ui.radioButton2.isChecked()):
        for i in range(0, 8):
           tmp.append(round(int(ui.table2020.item(i, 1).text()) * (100 + float(kTableValues[i])) / 100, 0))
    tmp.append(sum(tmp) - tmp[7])
    part = CalcPart(tmp)
    for i in range(0, 8):
        ui.tableResult.setItem(i, 0, QtWidgets.QTableWidgetItem(str(dict_analysis[i])))
        ui.tableResult.setItem(i, 1, QtWidgets.QTableWidgetItem(str(tmp[i])))
        ui.tableResult.setItem(i, 2, QtWidgets.QTableWidgetItem(str(round(part[i] * 100, 1)) + '%'))

    ui.tableResult.setItem(7, 0, QtWidgets.QTableWidgetItem(str(dict_analysis[7])))
    ui.tableResult.setItem(7, 1, QtWidgets.QTableWidgetItem(str(tmp[8])))
    ui.tableResult.setItem(7, 2, QtWidgets.QTableWidgetItem(str(round(tmp[8] / tmp[0] * 100, 1)) + '%'))

    ui.labelResult.setVisible(True)
    ui.tableResult.resizeColumnsToContents()
    ui.tableResult.resizeRowsToContents()
    ui.tableResult.setVisible(True)

def StartBalance(balance, year):
    df = pd.DataFrame(data = balance)
    if (year == 2019):
        ui.balancetable2019.setColumnCount(2)
        for i, row in df.iterrows():
            ui.balancetable2019.setRowCount(ui.balancetable2019.rowCount() + 1)

            for j in range(ui.balancetable2019.columnCount()):
                ui.balancetable2019.setItem(i, j, QtWidgets.QTableWidgetItem(str(row[j])))
            ui.balancetable2019.resizeColumnsToContents()
            ui.balancetable2019.resizeRowsToContents()
            ui.balancetable2019.verticalHeader().hide()
    else:
        ui.balancetable2020.setColumnCount(2)
        for i, row in df.iterrows():
            ui.balancetable2020.setRowCount(ui.balancetable2020.rowCount() + 1)

            for j in range(ui.balancetable2020.columnCount()):
                ui.balancetable2020.setItem(i, j, QtWidgets.QTableWidgetItem(str(row[j])))
            ui.balancetable2020.resizeColumnsToContents()
            ui.balancetable2020.resizeRowsToContents()
            ui.balancetable2020.verticalHeader().hide()

def GetCompanyList():
    global dirs
    example_dir = os.path.abspath(os.curdir)
    content = os.listdir(example_dir)
    dirs.clear()
    ui.comboBox.clear()
    for file in content:
        if os.path.isdir(os.path.join(example_dir, file)) and file.isnumeric():
            dirs.append(file)
    ui.comboBox.addItems(dirs)

def ComboBoxChanged():
    ui.lineEdit.setText(ui.comboBox.currentText())

GetCompanyList()
ui.comboBox.activated[str].connect(ComboBoxChanged)
ui.radioButton1.toggled.connect(radiobuttonchek)
ui.radioButton2.toggled.connect(radiobuttonchek)
ui.BtnDownload.clicked.connect(on_click)
ui.buttonResult.clicked.connect(CalcResultTable)
ui.buttonZLP.clicked.connect(linProg)


sys.exit(app.exec_())

# 2310031475