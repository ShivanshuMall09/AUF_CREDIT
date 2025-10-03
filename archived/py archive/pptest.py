# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 16:04:45 2022

@author: rajeev.jadaun
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 16:22:49 2020

@author: rajeev.jadaun
    AUF_CREDIT_Process_V.13.2.2.py:06-05-2022[replace varient name from CII-Young Indian to Zenith_CII_Young_Indian ] 
    AUF_CREDIT_Process_V.13.2.1.py:06-05-2022[adding artwork for  new bin 483974,483976,483894, also
                                              adding aler for bin 483974] 
    AUF_CREDIT_Process_V.13.1.2.py:06-05-2022[change pp expiry 3 years from date of processing] 
    AUF_CREDIT_Process_V.13.1.1.py:06-05-2022[adding artwork for EM_B466505_L102_G0] 
    AUF_CREDIT_Process_V.13.1.1.py:06-05-2022[adding artwork for EM_B466505_L102_G0] 
    AUF_CREDIT_Process_V.13.1.0.py:21-04-2022[new bin addition]
    AUF_CREDIT_Process_V.12.1.0.py:21-04-2022[Removing add on pp of vetta varient as per customer requirement]
    AUF_CREDIT_ProcessV.11.2.0.py:21-12-2021[Batch card info change(artwork)]



"""
import os
import time
import glob
import random
import datetime
import hashlib

from datetime import date

primary_card = []
secondary_card = []
places = []
cardnumber_list=[]
bin_list=[]
pp_list=[]
records_list=[]
records_list_acc=[]
ps_list = []
ps1_list = []
pps_list = []
p_acc_card_count =[]
s_acc_card_count = []
s_acc_card_count1 = []
pp_dup_check =[]

ts = datetime.datetime.now()
ptime = ts.strftime("%d.%m.%Y_%H%M%S")


with open('config/AUC_batch_series', 'r') as fin:
    batch_series_data = fin.read().splitlines(True)
    batch_series = batch_series_data[0:1]

with open('config/AUC_batch_series', 'w') as fout:
    fout.writelines(batch_series_data[1:])
listToStr = ' '.join([str(elem) for elem in batch_series])
batch_number = listToStr[0:5]

file_name = glob.glob('L2CDZU*')
for fn in file_name:
    with open((fn), 'r') as filehandle:
        filecontents = filehandle.readlines()
        del filecontents[0]
        del filecontents[-1]
        ts = time.time( )
        x = (ts)
        #filenames = glob.glob('L2CDZU*')
        merge_output_file = 'del_output_file_'+str(x)+'_.txt'
        with open(merge_output_file, 'a') as outfile:
            for fname in filecontents:
                outfile.write(fname)
    filehandle.close()                 
merge_filename = glob.glob('del_output_file*.txt')
with open('merge_output_file_'+str(x)+'.txt', 'w') as outfile:
    for fname in merge_filename:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)
                records_list.append(line)

                for i in enumerate(line):
                    account_number = line[38:54]
                    file_credit_card_em = line[:]
                    
                with open('AUC_EM_account_'+str(account_number)+'_'+str(ptime)+'.txt', 'a') as em_file:
                    em_file.write(file_credit_card_em)
                em_file.close()  
outfile.close()

auf_pp_output_header = 'Account_Number,Logo,Card_Number,Card_Holder_name,Card_action,Priority_Pass_Number,PP_issuance_date' 

with open('Priority_Pass_Data_'+str(ptime[0:10])+'.csv', 'w') as pp_file_auf_h:
    pp_file_auf_h.write(auf_pp_output_header +'\n')
                #print (file_pp_merge)
pp_file_auf_h.close()
    
def jdtodatestd (jdate):
    jdate=str(jdate)
    datestd = datetime.datetime.strptime(jdate, '%Y%j' ).date()
    return(datestd)  

merge_filename_acc = glob.glob('*account*')
with open('M_account_file_'+str(x)+'.txt', 'w') as outfile_acc:
    for fname_acc in merge_filename_acc:
        with open(fname_acc) as infile_acc:
            for line_acc in infile_acc:
                outfile_acc.write(line_acc)
                records_list_acc.append(line_acc)
                s_no1= (records_list.index(line_acc))   
                s_no = "%03d" % s_no1
                
                for i in enumerate(line_acc):
                    logo_acc = line_acc[3:6]
                    c_bin_f_acc = line_acc[9:15]
                    #print(c_bin_f_acc,logo_acc)
                    account_number_acc = line_acc[38:54]
                    print_card_holder_name_acc = line_acc[54:80].rstrip()
                    pct_id = line_acc[501:504]
                    card_holder_name_acc = line_acc[1518:1558]
                    date_acc = line_acc[2659:2666]
                    card_holder_firstname_acc = line_acc[2763:2803].rstrip()
                    card_holder_middlename_acc = line_acc[2803:2843].rstrip()
                    card_holder_lastname_acc = line_acc[2843:2883].rstrip()
                    plastic_id = line_acc[402:412]
                    #salutation_acc = line_acc[2090:2094].rstrip()
                    card_holder_type_acc = line_acc[2089:2090]        
                    cardnumber_acc = line_acc[9:25]
                    mask_pan_acc = cardnumber_acc[0:6]+'XXXXXX'+cardnumber_acc[12:16]
                    c_bin_acc = line_acc[9:15]
                    #print(c_bin_acc)
                    f_bin_acc = line_acc[9:15]
                    pp1_acc = line_acc[18:25]
                    print(pp1_acc)
                    pp2_reverse_acc=pp1_acc[::-1]
                    pp3_rand_acc = random.choices(pp2_reverse_acc, k=7)
                    pp4_acc = ''.join(map(str, pp3_rand_acc))
                    
                    ppnum1 = random.random()
                    
                    ppnum2 = str(ppnum1).replace("0.","")
                    ppnum3 = random.choices(ppnum2, k=13)
                    ppnum4 = ''.join(map(str, ppnum3))

                    ppnum5 = (pp4_acc)+(ppnum4)
                    ppnum6 = random.choices(str(ppnum5), k=7)
                    ppnum7 = ''.join(map(str, ppnum6))
                    
#--------------------------pp dup check--------------------------  
                  #  with open('config/pp_db', 'a') as pp_dup:
                  #      pp_dup.write(ppnum7+'\n')
                  #  pp_dup.close()    
                    
                    
#-----------------------------------------------------------------------------------------
                    
                    
                    
                    
                    
                    pp_cardnumber_acc = c_bin_acc+'999'+str(ppnum7)
                    print(pp_cardnumber_acc)
                    
                 
outfile_acc.close()  
