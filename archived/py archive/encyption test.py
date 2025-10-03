# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 19:48:23 2022

@author: Administrator
"""
import jpype
import asposecells
jpype.startJVM()
from asposecells.api import *
from py4j.java_gateway import JavaGateway 
gateway = JavaGateway() 
# Load XLSX workbook
wb = Workbook("B:/DATA-FILES/LIVE/AUF CREDIT/WORKING_FOLDER/AUC_TEST/test/AUF_Credit_Bluedart_Courier_Connection_Report_00321_18.07.2022_191633.xlsx")
# Load XLSX workbook
#wb = Workbook("workbook.xlsx")

# Password protect Excel file
wb.getSettings().setPassword("1234")

# Encrypt by specifying the encryption type
wb.setEncryptionOptions(EncryptionType.XOR, 40)

# Specify Strong Encryption type (RC4,Microsoft Strong Cryptographic Provider)
wb.setEncryptionOptions(EncryptionType.STRONG_CRYPTOGRAPHIC_PROVIDER, 128)

# Save Excel file
wb.save("B:/DATA-FILES/LIVE/AUF CREDIT/WORKING_FOLDER/AUC_TEST/test/workbook-encrypted.xlsx")