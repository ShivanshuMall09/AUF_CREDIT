# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 13:47:46 2022

@author: rajeev.jadaun
"""

import pandas as pd
import numpy as np
import xlwings as xw
import matplotlib.pyplot as plt

excel_file = ''
df = pd.read_csv(r"AUF_Credit_Data_Allocation_Report_00030_08.06.2022_175825.xlsx")
                 
wb = xw.Book()
sht = wb.sheets["Sheet1"]
sht.name = "fruit_and_veg_sales"
sht.range("A1").options(index=False).value = df

wb.sheets.add('Dashboard')
sht_dashboard = wb.sheets('Dashboard')