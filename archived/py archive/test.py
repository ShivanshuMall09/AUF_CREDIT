# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 15:39:19 2022

@author: rajeev.jadaun
"""
import pandas as pd

df = pd.read_csv('AUF_Credit_Delhivery_Courier_Connection_Report_.txt',encoding= 'unicode_escape', sep='|', dtype=object)
df.to_excel('AUF_Credit_Delhivery_Courier_Connection_Report_.xlsx', 'Sheet1',index=False)