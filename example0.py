# -*- coding: utf-8 -*-

from autocadscript import AScript, APoint

import os
import sys
import math
import xlrd

def open_excel(file):
    """打开EXCEL表格"""
    try:
        book = xlrd.open_workbook(file)
        return book
    except Exception as error_code:
        print(error_code)

def get_sheet_by_index(file, sheet_index):
    """根据表的索引 sheet_index 获取 EXCEL 文件中的表"""
    book = open_excel(file)
    table = book.sheet_by_index(sheet_index)
    nrows = table.nrows
    ncols = table.ncols
    sheet = []
    for j in range(0, nrows):
        row = []
        for i in range(0, ncols):
            row.append(table.cell_value(j, i))
        sheet.append(row)
    return sheet

FILE_PATH = sys.path[0]
os.chdir(FILE_PATH)
print('路径：' + FILE_PATH)
sheet = get_sheet_by_index("Test.xlsx", 0)

line_number = sheet[0]
d = sheet[1]
V = sheet[2]
Delta = sheet[3]
A_w = sheet[4]
X_f = sheet[5]
X_b = sheet[6]
Z_b = sheet[7]
Z_mL = sheet[8]
Delta_cm = sheet[9]
M_cm = sheet[10]
C_w = sheet[11]
C_m = sheet[12]
C_b = sheet[13]
C_p = sheet[14]

A = AScript()
points_list = []
for i in range(1, len(sheet)):
    pline = []
    for j in range(1, len(sheet[i])):
        pline.append(APoint(sheet[0][j], sheet[i][j]).multiply(i * 50))
    points_list.append(pline)
    A.draw_pline(pline)

A.layer_add('TT')

A.create(FILE_PATH, 'TEST')
