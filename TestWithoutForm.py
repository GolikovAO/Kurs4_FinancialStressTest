import requests
import json
import zipfile
import fnmatch
import pandas as pd
import numpy as np
import csv
import openpyxl
import Organization
import  os


def WorkWithExcelPandas(org):
    data_xls = pd.read_excel(org.excel_filename, sheet_name='Financial Result', header=None)
    data_xls.dropna()
    data_xls.to_csv('your_csv.csv', encoding='utf-8')

def WorkWithExcelOpenpyxl(org):
    wb = openpyxl.load_workbook(org.excel_filename)
    sheet = wb['Financial Result']
    with open('csv.csv', 'a', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for row in sheet['A7':'BA27']:
            tmp_list = []
            for cell in row:
                if (cell.value != None):
                 tmp_list.append(cell.value)
            if (tmp_list):
                writer.writerow(tmp_list[1:])


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

dict_analysis = ['Выручка', 'Себестоимость проданных товаров', 'Административные и коммерческие расходы', 'Сальдо процентов по кредиту',
                 'Прочие доходы-расходы', 'Прочее (другие доходы-расходы)', 'Налог на прибыль', 'Чистая прибыль']


def CalcPart(list):
    tmp = []
    for i in range(0, 8):
        tmp.append(round(list[i] / list[0], 3))
    return tmp

# org1 = Organization.Organization('6432009756')
# org1 = Organization.Organization('2310031475')
# org1.GetNameAndAddress()
# balance1 = org1.GetBalance2019()
# balance2 = org1.GetBalance2020()
# print(len(balance1))
# for row in balance1:
#     print(row)
# print(len(balance2))
# for row in balance2:
#     print(row)
# data2019 = org1.Get2019DataFromExcel()
# data2020 = org1.Get2020DataFromExcel()
# data2020 = ReworkList(data2020)
# data2019 = ReworkList(data2019)
# print(data2019)
# print(data2020)
#
# part2019 = CalcPart(data2019)
# part2020 = CalcPart(data2020)
# print(part2019)
# print(part2020)

example_dir = os.path.abspath(os.curdir)
content = os.listdir(example_dir)
dirs = []
for file in content:
    if os.path.isdir(os.path.join(example_dir, file)) and file.isnumeric():
        dirs.append(file)

