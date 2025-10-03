
"""
Created on Thu Nov  5 16:22:49 2020

@author: rajeev.jadaun
      AUF_CREDIT_ProcessV.15.3.2.py:28-07-2022[Data deletion form]
      AUF_CREDIT_ProcessV.15.3.1.py:23-07-2022[Delhivery Excel generation] 
      AUF_CREDIT_ProcessV.15.2.1.py:19-07-2022[handeled special character in input file] 
      AUF_CREDIT_ProcessV.15.1.1.py:1-07-2022[Progress report in console, error msg handling without closuing the exe]
      AUF_CREDIT_ProcessV.14.1.1.py:18-06-2022[replace file handling] 
      
      
      AUF_CREDIT_Process_V.13.3.1.py:01-06-2022[add a function to check the pp dp check]
      AUF_CREDIT_Process_V.13.2.3.py:01-06-2022[adding artwork for G0 product for all ALTURA varients] 
      AUF_CREDIT_Process_V.13.2.2.py:06-05-2022[replace varient name from CII-Young Indian to Zenith_CII_Young_Indian ] 
      AUF_CREDIT_Process_V.13.2.1.py:06-05-2022[adding artwork for  new bin 483974,483976,483894, also
                                                adding aler for bin 483974] 
      AUF_CREDIT_Process_V.13.1.2.py:06-05-2022[change pp expiry 3 years from date of processing] 
      AUF_CREDIT_Process_V.13.1.1.py:06-05-2022[adding artwork for EM_B466505_L102_G0] 
      AUF_CREDIT_Process_V.13.1.1.py:06-05-2022[adding artwork for EM_B466505_L102_G0] 
      AUF_CREDIT_Process_V.13.1.0.py:21-04-2022[new bin addition]
      AUF_CREDIT_Process_V.12.1.0.py:21-04-2022[Removing add on pp of vetta varient as per customer requirement]
      AUF_CREDIT_ProcessV.11.2.0.py:21-12-2021[Batch card info change(artwork)]
      
      
      AUF_CREDIT_ProcessV.11.3.0.py:11-01-2022[Full automation]
      AUF_CREDIT_ProcessV.11.2.0.py:21-12-2021[Batch card info change(artwork)]
         


"""


import os
import time
import glob
import random
import datetime
import hashlib
from pathlib import Path
from datetime import date
import pandas as pd
from babel.numbers import format_currency
import traceback
try:
    print("DATA PROCESSING STARTS.....")
    #del_file1 = glob.glob("*.txt*")
    
    
    primary_card = []
    secondary_card = []
    places = []
    cardnumber_list = []
    bin_list = []
    pp_list = []
    # records_list=[]
    records_list_acc = []
    ps_list = []
    ps1_list = []
    pps_list = []
    p_acc_card_count = []
    s_acc_card_count = []
    s_acc_card_count1 = []
    pp_dup_check = []
    bd_num = 0
    dl_num = 0
    ip_num = 0
    
    awb_number = 0
    awb_number_bd = []
    awb_number_dl = []
    awb_number_ip = []
    routing_code = ''
    courier = ''
    row = []
    account_number_list = []
    records_list = []
    s_no = 0
    pp_count=''
    total_primary_count = 0
    total_pp_count = 0
    count = 0
    
    
    ts = datetime.datetime.now()
    ptime = ts.strftime("%d.%m.%Y_%H%M%S")
    print(ptime)
    
    
    with open('config/AUC_batch_series', 'r') as fin:
        batch_series_data = fin.read().splitlines(True)
        batch_series = batch_series_data[0:1]
    with open('config/AUC_batch_series', 'w') as fout:
        fout.writelines(batch_series_data[1:])
    listToStr = ' '.join([str(elem) for elem in batch_series])
    batch_number = listToStr[0:5]
    fout.close()
    
    with open('config/BD_AWB.txt', 'r') as bdfin, open('config/BD_AWB_USING.txt', 'w') as bdfout:
        contents = bdfin.readlines()
        bdfout.writelines(contents)
    bdfin.close()
    bdfout.close()
    with open('config/DL_AWB.txt', 'r') as dtfin, open('config/DL_AWB_USING.txt', 'w') as dtfout:
        contents = dtfin.readlines()
        dtfout.writelines(contents)
    dtfin.close()
    dtfout.close()
    with open('config/IP_AWB.txt', 'r') as ipfin, open('config/IP_AWB_USING.txt', 'w') as ipfout:
        contents = ipfin.readlines()
        ipfout.writelines(contents)
    ipfin.close()
    ipfout.close()
    
    # sorting defination for EMBOSSA file
    
    
    def my_sort_emb(line):
        line_fields = line.strip().split()
        couriersort = line_fields[-1]
        
        return couriersort
    
    def pp_sort_emb(line):
        line_fields = line.strip().split()
        couriersort = line_fields[-1]
        couriersort = couriersort[-1]
        print(couriersort)
        return couriersort
        # print(cabin_class)
    
    # sorting defination for FF_MIS file
    
    
    def my_sort_ff(line):
        line_fields = line.strip().split('|')
        couriersort = (line_fields[14])
        return couriersort
    
    def my_sort_pp(line):
        line_fields = line.strip().split('|')
        couriersort = (line_fields[11])
        print(couriersort)
        return couriersort
    
    def pp_dup_check(number):
        with open('./config/AUF_CREDIT_PP_CONSOLE.txt','r+') as file_read:
            contents = file_read.readlines()
            new_contents = [x[:-1] for x in contents]
            #contents = contents.replace("\n","")
            
            #(number)
            #print(new_contents)
            #number = int(number)
            #number_check = number+"\n"
            if number in new_contents:
                print("PP duplicate number found : "+number)
                
                file_read.close()
                number = int(number)+100
                #print("PP duplicate found :")
                return(pp_dup_check(str(number)))
                
                
            else:
                #    ("not found")
                file_read.write(number+'\n')
                file_read.close()
                return number
            
    file_name = glob.glob('L2CDZU*')
    for fn in file_name:
        with open((fn), 'r') as filehandle:
            filecontents = filehandle.readlines()
            del filecontents[0]
            del filecontents[-1]
            ts = time.time()
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
    
                    #with open('AUC_EM_account_'+str(account_number)+'_'+str(ptime)+'.txt', 'a') as em_file:
                    with open('AUC_EM_account.txt', 'a') as em_file:
                        em_file.write(file_credit_card_em)
                    em_file.close()
    outfile.close()
    
    auf_pp_output_header = 'Account_Number,Logo,Card_Number,Card_Holder_name,Card_action,Priority_Pass_Number,PP_issuance_date'
    
    with open('Priority_Pass_Data_'+str(ptime[0:10])+'.csv', 'w') as pp_file_auf_h:
        pp_file_auf_h.write(auf_pp_output_header + '\n')
        
        #print (file_pp_merge)
    pp_file_auf_h.close()
    
    
    def jdtodatestd(jdate):
        jdate = str(jdate)
        datestd = datetime.datetime.strptime(jdate, '%Y%j').date()
        datestd = str(datestd)
    
        if datestd[5:7] == '01':
            month = 'Jan'
        elif datestd[5:7] == '02':
            month = 'Feb'
        elif datestd[5:7] == '03':
            month = 'Mar'
        elif datestd[5:7] == '04':
            month = 'Apr'
        elif datestd[5:7] == '05':
            month = 'May'
        elif datestd[5:7] == '06':
            month = 'Jun'
        elif datestd[5:7] == '07':
            month = 'Jul'
        elif datestd[5:7] == '08':
            month = 'Aug'
        elif datestd[5:7] == '09':
            month = 'Sep'
        elif datestd[5:7] == '10':
            month = 'Oct'
        elif datestd[5:7] == '11':
            month = 'Nov'
        elif datestd[5:7] == '12':
            month = 'Dec'
    
        plastic_issue_date = (datestd[8:10]+'-'+month+'-'+datestd[0:4])
        return(plastic_issue_date)
    
    
    count = 0
    merge_filename_acc = glob.glob('*account*')
    with open('M_account_file_'+str(x)+'.txt', 'w') as outfile_acc:
        for fname_acc in merge_filename_acc:
            with open(fname_acc) as infile_acc:
                for line_acc in infile_acc:
                    outfile_acc.write(line_acc)
                    line=line.replace('â€™', "'")
                    line=line.replace('|', " ")
                    line=line.replace('â€œ', " ")
                    line=line.replace('”', " ")
                    line=line.replace('“', " ")
                    line=line.replace('"', " ")
                    line=line.replace('…', " ")
                    records_list_acc.append(line_acc)
                    s_no1 = (records_list.index(line_acc))
                    s_no = "%03d" % s_no1
    
                    for i in enumerate(line_acc):
                        
    
                        logo_acc = line_acc[3:6]
                        c_bin_f_acc = line_acc[9:15]
                        account_number_acc = line_acc[38:54]
                        # account_number_list.append(account_number_acc)
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
                        mask_pan_acc = cardnumber_acc[0:6] +'XXXXXX'+cardnumber_acc[12:16]
                        c_bin_acc = line_acc[9:15]
                        f_bin_acc = line_acc[9:15]
                        pp1_acc = line_acc[18:25]
                        pp2_reverse_acc = pp1_acc[::-1]
                        pp3_rand_acc = random.choices(pp2_reverse_acc, k=7)
                        pp4_acc = ''.join(map(str, pp3_rand_acc))
    
                        
    
                        print_exp_date_acc = line_acc[162:164] +'/'+line_acc[164:166]
                        pp_exp_date_acc = ptime[3:5]+ptime[8:10] #ADDED ON 23052022 AS PER CUSTOMER REQUIREMENT FOR CARD EXPIRY OF 3 YEARS
                        gender_code_acc = line_acc[2103:2104]
                        customer_id_acc1 = line_acc[1134:1153].lstrip()
                        customer_id_acc = customer_id_acc1.rstrip()
                        cr_card_limit = line_acc[167:182]
                        cr_card_limit = cr_card_limit.lstrip('0')
                        cr_card_limit = format_currency(cr_card_limit, '', locale='en_IN')
                        #cr_card_limit = format_currency(cr_card_limit, 'INR', locale='en_IN') #"INR" for indian rupee logo
                        #cr_card_limit=str(cr_card_limit)+'.00'
                        card_action_code = line_acc[150:151]
                        billing_cycle = line_acc[3844:3846]
                        billing_cycle_int = int(billing_cycle)
                        add_on_mask_pan = ''
                        tile_acc = line_acc[1938:1958].rstrip()
                        mailer_name1_acc = line_acc[1518:1558].rstrip()
                        mailer_name2_acc = line_acc[1558:1598].rstrip()
                        mailer_name3_acc = line_acc[1598:1638].rstrip()
                        mailer_name_acc = mailer_name1_acc+' '+mailer_name2_acc+' '+mailer_name3_acc
                        mailer_address1_acc = line_acc[1638:1678].rstrip()
                        mailer_address2_acc = line_acc[1678:1718].rstrip()
                        mailer_address3_acc = line_acc[1718:1758].rstrip()
                        mailer_address4_acc = line_acc[1878:1918].rstrip()
                        mailer_city_acc = line_acc[1758:1788].rstrip()
                        mailer_state_code_acc = line_acc[1838:1868].rstrip()
                        mailer_postal_code_acc = line_acc[2016:2026].rstrip()
                        mailer_mob_acc = line_acc[3143:3163].rstrip() 
                        suffix = ""
                        pp_cardnumber_acc = "'NA"
                        
                        if ((c_bin_acc == '465523' and card_holder_type_acc=='1') or c_bin_acc == '457036'):
                            if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):                    
                                ppnum1 = random.random()
                                ppnum2 = str(ppnum1).replace("0.", "")
                                ppnum3 = random.choices(ppnum2, k=13)
                                ppnum4 = ''.join(map(str, ppnum3))
                                ppnum5 = (pp4_acc)+(ppnum4)
                                ppnum6 = random.choices(str(ppnum5), k=7)
                                ppnum7 = ''.join(map(str, ppnum6))
                                pp_cardnumber_acc = c_bin_acc+'999'+str(ppnum7)
                        
                        if gender_code_acc == '1':
                            salutation_acc = 'Mr.'
                        elif gender_code_acc == '2':
                            salutation_acc = 'Ms.'
                        else:
                            salutation_acc = 'Not Found'
    
                        
                        if 4 <= billing_cycle_int <= 20 or 24 <= billing_cycle_int <= 30:
                            suffix = "th"
                        else:
                            suffix = ["st", "nd", "rd"][billing_cycle_int % 10 - 1]
                        superscript = suffix
    
                        if card_action_code == '1':
                            card_action = 'New Issue'
                        elif card_action_code == '2':
                            card_action = 'Additional Card'
                        elif card_action_code == '3':
                            card_action = 'Replacement Card'
                        elif card_action_code == '4':
                            card_action = 'Return Card'
                        elif card_action_code == '6':
                            card_action = 'Emergency Card Requested'
                        elif card_action_code == '7':
                            card_action = 'Reissue Card'
                        elif card_action_code == '8':
                            card_action = 'Reissue Card with different card numbering scheme'
                        elif card_action_code == '9':
                            card_action = 'Card technology reissue'
                        elif card_action_code == 'A':
                            card_action = 'Additional Card'
                        elif card_action_code == 'L':
                            card_action = 'Lost and Stolen Replacement'
                        elif card_action_code == '0':
                            card_action = 'No Action Requested'
                        else:
                            card_action = 'No action code matched'
    
                        if plastic_id == '0000000002':
                            celeb = 'C_Male'
                        elif plastic_id == '0000000003':
                            celeb = 'C_Female'
                        else:
                            celeb = ''
                        j_ts = date.today()
                        j_x = (j_ts)
                        j_fmt = '%Y-%m-%d'
                        j_s = str(j_x)
                        j_dt = datetime.datetime.strptime(j_s, j_fmt)
                        j_tt = j_dt.timetuple()
                        j_tt.tm_yday
                        j_p = int('%d%03d' % (j_tt.tm_year, j_tt.tm_yday))
                        j_day = str(j_p)
    
                        ref_number = customer_id_acc[2:]+card_holder_name_acc[0:4].upper()+j_day[4:7]+j_day[0:4]+str(s_no)
                        if card_holder_type_acc == '1':
                            card_type = 'Primary Card'
                            # account_number_list.append(account_number_acc)
                        elif card_holder_type_acc == '0':
                            card_type = 'Add-on  Card'
    
                        ps = account_number_acc+'|'+card_type
                        pps = [account_number_acc, mask_pan_acc]
    
                        if c_bin_acc == '466505'  and  logo_acc == '101': 
                            if plastic_id == '          ':
                                varient = 'Altura'
                            elif plastic_id == '0000000002':
                                varient = 'Altura_Celeb_Male'
                            elif plastic_id == '0000000003':
                                varient = 'Altura_Celeb_Female'
                            else:
                                varient ='Not Found'
                            
                        elif c_bin_acc == '466505'  and  logo_acc == '102':
                            if gender_code_acc == '0':
                                varient = 'AlturaPlusBlue'
                            elif gender_code_acc == '1':
                                varient = 'AlturaPlusBlue'
                            elif gender_code_acc == '2':
                                varient = 'AlturaPlusRuby'
                        
                        elif c_bin_acc == '465523'  and  logo_acc == '301': 
                            varient = 'Vetta'
                        
                        elif c_bin_acc == '457036'  and  logo_acc == '401': 
                            #ADDED on 26052022 as per customer requiement new varient
                            #young indians with pastic id 
                            if plastic_id == '          ':
                                varient = 'Zenith'
                            elif plastic_id == '0000000001':
                                varient = 'Zenith_CII_Young_Indian'
                            
                            
                        #New BIN ADDITON-21-04-2022
                        elif c_bin_acc == '406977'  and  logo_acc == '501':
                            varient = 'AU_BANK_LIT_CREDIT_CARD'
                        
                        elif c_bin_acc == '483976'  and  logo_acc == '601':
                            varient = 'Corporate_Reward_Credit Card'
                        elif c_bin_acc == '483976'  and  logo_acc == '602':
                            varient = 'Corporate_Credit_Card'
                        elif c_bin_acc == '483976'  and  logo_acc == '603':
                            varient = 'Secured_Corporate_Credit_Card'
                        
                        elif c_bin_acc == '483974'  and  logo_acc == '701':
                            varient = 'Purchase Reward Credit Card'
                        elif c_bin_acc == '483974'  and  logo_acc == '702':
                            varient = 'Purchase Credit Card'
                        elif c_bin_acc == '483974'  and  logo_acc == '703':
                            varient = 'Secured_Purchase_Credit_Card'
                        
                        elif c_bin_acc == '483894'  and  logo_acc == '801':
                            varient = 'Business_Reward_Credit_Card'
                        elif c_bin_acc == '483894'  and  logo_acc == '802':
                            varient = 'Secured Business Credit Card'
                        elif c_bin_acc == '483894'  and  logo_acc == '803':
                            varient = 'Business Cashback Credit Card'
    
                        
                        if logo_acc == '101' and pct_id == '101':
                            joining_fees = 'NIL'
                            annual_fees = 'NIL'
                        elif logo_acc == '101' and pct_id == '001':
                            joining_fees = '199'
                            annual_fees = '199'
                        elif logo_acc == '101' and pct_id == '102':
                            joining_fees = 'NIL'
                            annual_fees = '199'
    
                        elif logo_acc == '102' and pct_id == '103':
                            joining_fees = 'NIL'
                            annual_fees = 'NIL'
                        elif logo_acc == '102' and pct_id == '003':
                            joining_fees = '499'
                            annual_fees = '499'
                        elif logo_acc == '102' and pct_id == '104':
                            joining_fees = 'NIL'
                            annual_fees = '499'
    
                        elif logo_acc == '103' and pct_id == '029':
                            joining_fees = '299'
                            annual_fees = '299'
                        elif logo_acc == '103' and pct_id == '100':
                            joining_fees = 'NIL'
                            annual_fees = '299'
                        elif logo_acc == '103' and pct_id == '109':
                            joining_fees = 'NIL'
                            annual_fees = 'NIL' 
    
                        elif logo_acc == '301' and pct_id == '105':
                            joining_fees = 'NIL'
                            annual_fees = 'NIL'
                        elif logo_acc == '301' and pct_id == '007':
                            joining_fees = '2,999'
                            annual_fees = '2,999'
                        elif logo_acc == '301' and pct_id == '106':
                            joining_fees = 'NIL'
                            annual_fees = '2,999'
    
                        elif logo_acc == '302' and pct_id == '009':
                            joining_fees = '1,499'
                            annual_fees = '1,499'
                        elif logo_acc == '302' and pct_id == '112':
                            joining_fees = 'NIL'
                            annual_fees = '1,499'
                        elif logo_acc == '302' and pct_id == '113':
                            joining_fees = 'NIL'
                            annual_fees = '749'
                        elif logo_acc == '302' and pct_id == '114':
                            joining_fees = 'NIL'
                            annual_fees = '2,999'
                        elif logo_acc == '302' and pct_id == '010':
                            joining_fees = '749'
                            annual_fees = '749'
                        elif logo_acc == '302' and pct_id == '030':
                            joining_fees = '2,999'
                            annual_fees = '2,999'
                        elif logo_acc == '302' and pct_id == '111':
                            joining_fees = 'NIL'
                            annual_fees = 'NIL'
                        
    
                        elif logo_acc == '303' and pct_id == '115':
                            joining_fees = 'NIL'
                            annual_fees = 'NIL'
    
                        elif logo_acc == '401' and pct_id == '107':
                            joining_fees = 'NIL'
                            annual_fees = 'NIL'
                        elif logo_acc == '401' and pct_id == '012':
                            joining_fees = '7,999'
                            annual_fees = '7,999'
                        elif logo_acc == '401' and pct_id == '108':
                            joining_fees = 'NIL'
                            annual_fees = '7,999'
                        
                        elif logo_acc == '501' and pct_id == '031':
                            joining_fees = '99'
                            annual_fees = '99'
                        elif logo_acc == '501' and pct_id == '116':
                            joining_fees = 'NIL'
                            annual_fees = 'NIL'
                        
                        elif logo_acc == '601' and pct_id == '015':
                            joining_fees = 'NIL'
                            annual_fees = 'NIL'
                        
                        elif logo_acc == '602' and pct_id == '016':
                            joining_fees = 'NIL'
                            annual_fees = 'NIL'
                        
                        elif logo_acc == '603' and pct_id == '017':
                            joining_fees = 'NIL'
                            annual_fees = 'NIL'
                        
                        elif logo_acc == '701' and pct_id == '018':
                            joining_fees = 'NIL'
                            annual_fees = 'NIL'
                        
                        elif logo_acc == '702' and pct_id == '019':
                            joining_fees = 'NIL'
                            annual_fees = 'NIL'
                        
                        elif logo_acc == '703' and pct_id == '020':
                            joining_fees = 'NIL'
                            annual_fees = 'NIL'
                        
                        elif logo_acc == '801' and pct_id == '022':
                            joining_fees = 'NIL'
                            annual_fees = 'NIL'
                        
                        elif logo_acc == '802' and pct_id == '023':
                            joining_fees = 'NIL'
                            annual_fees = 'NIL'
                        
                        elif logo_acc == '803' and pct_id == '024':
                            joining_fees = 'NIL'
                            annual_fees = 'NIL'
                        elif logo_acc == '803' and pct_id == '025':
                            joining_fees = '999'
                            annual_fees = '999'
                        elif logo_acc == '803' and pct_id == '026':
                            joining_fees = '499'
                            annual_fees = '499'
                        elif logo_acc == '803' and pct_id == '027':
                            joining_fees = 'NIL'
                            annual_fees = '999'
                        elif logo_acc == '803' and pct_id == '028':
                            joining_fees = 'NIL'
                            annual_fees = '499'
                        
                        file_credit_card_ff_acc = ' '+'|'+c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+ref_number+'|'+card_type+'|'+mask_pan_acc+'|'+account_number_acc+'|'+card_action+'|'+salutation_acc+'|'+mailer_name_acc+'|'+mailer_address1_acc+'|'+mailer_address2_acc+'|' + mailer_address3_acc+'|'+mailer_address4_acc+'|'+mailer_city_acc+'|'+mailer_state_code_acc+'|'+mailer_postal_code_acc+'|'+mailer_mob_acc+'|' + customer_id_acc+'|'+cr_card_limit+'|'+billing_cycle+'|'+superscript+'|' + print_card_holder_name_acc+'|' +  pct_id+'|'  # +jdtodatestd(date_acc)
                        
                        file_credit_card_ff_acc_allocation = ' '+'|'+account_number_acc + '|'+mask_pan_acc+'|'+mailer_name_acc+'|'+'|'+'|'+'|'+'|'
                        file_credit_card_ff_acc_primary = ' '+'|'+account_number_acc + '|'+mask_pan_acc+'|'+mailer_name_acc+'|'+'|'+'|'+'|'+'|'
                        file_credit_card_ff_acc_addon = ' '+'|'+account_number_acc + '|'+'|'+mailer_name_acc+'|'+mask_pan_acc+'|'+'|'+'|'+'|'
                        file_credit_card_ff_acc_3_primary = card_action+'|'+'1|'+'0|'+'1|'+c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+mailer_address1_acc+'|'+mailer_address2_acc+'|'+mailer_address3_acc+'|'+mailer_address4_acc+'|'+mailer_city_acc + '|'+mailer_state_code_acc+'|'+mailer_postal_code_acc+'|'+mailer_mob_acc+'|'+customer_id_acc+'|'+cr_card_limit+'|' + billing_cycle+'|'+superscript+'|'+print_card_holder_name_acc + '|'+joining_fees+'|'+annual_fees + '|'+str(jdtodatestd(date_acc))
                        file_credit_card_ff_acc_3_primary_replace = card_action+'|'+'1|'+'0|'+'1|'+c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+mailer_address1_acc+'|'+mailer_address2_acc+'|'+mailer_address3_acc+'|'+mailer_address4_acc+'|'+mailer_city_acc + '|'+mailer_state_code_acc+'|'+mailer_postal_code_acc+'|'+mailer_mob_acc+'|'+customer_id_acc+'|'+cr_card_limit+'|' + billing_cycle+'|'+superscript+'|'+print_card_holder_name_acc
                        file_credit_card_ff_acc_3_addon = card_action+'|'+'0|'+'1|'+'1|'+c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+mailer_address1_acc+'|'+mailer_address2_acc+'|'+mailer_address3_acc+'|'+mailer_address4_acc+'|'+mailer_city_acc +'|'+mailer_state_code_acc+'|'+mailer_postal_code_acc+'|'+mailer_mob_acc+'|'+customer_id_acc+'|'+cr_card_limit+'|' +billing_cycle+'|'+superscript+'|'+print_card_holder_name_acc +'|'+joining_fees+'|'+annual_fees +'|'+str(jdtodatestd(date_acc))
                        file_credit_card_ff_acc_3_addon_replace = card_action+'|'+'0|'+'1|'+'1|'+c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+mailer_address1_acc+'|'+mailer_address2_acc+'|'+mailer_address3_acc+'|'+mailer_address4_acc+'|'+mailer_city_acc +'|'+mailer_state_code_acc+'|'+mailer_postal_code_acc+'|'+mailer_mob_acc+'|'+customer_id_acc+'|'+cr_card_limit+'|' +billing_cycle+'|'+superscript+'|'+print_card_holder_name_acc 
                        indianpost_courier_1 = '||'+ref_number+'|'+mailer_city_acc+'|'+mailer_postal_code_acc+'|'+mailer_name_acc+'|' + mailer_address1_acc+'|'+mailer_address2_acc+'|'+mailer_address3_acc + '|'+mailer_address4_acc+'|'+mailer_mob_acc+'||'
                        file_credit_card_ff_acc_new = ' '+'|'+account_number_acc+'|'+ref_number+'|'+mask_pan_acc+'|'+salutation_acc+' '+mailer_name_acc + '|'+pp_cardnumber_acc+'|'+print_exp_date_acc+'|'+varient + '|'+logo_acc+'|' + gender_code_acc  # +jdtodatestd(date_acc)
                        file_credit_card_em_acc = line_acc[:].rstrip('\n')
                        #header='Sr. No|Account Number|Primary Card number|Customer Name|Add-on Card 1|Add-on Card 2|Add-on Card 3|Add-on Card 4|PP  Card No_Primary|PP  Card No_Addon1|PP  Card No_Addon2|PP  Card No_Addon3|Ref no.|AWB. No.|Courier|Courier Code|Card Action|Primary Count|Add-on Count|Total Cards|Bin|Logo|Gender Code|Varient|Address Line 1|Address Line 2|Address Line 3|Address Line 4|City|State Code|Postal Code|Mobile Number|Cust Unique ID|Credit Limit|Statement Date |Extention|Embo_Name|Joining Fees|Annual Fees|Card Issuance Date'
                        bin_list.append(c_bin_acc+logo_acc+gender_code_acc)
                        bin_list = list(dict.fromkeys(bin_list))
                        qty = ''
    
                        #ps1 = account_number_acc+'|'+card_type+'|'+account_number_acc+'|'+mask_pan_acc+'|'+mailer_name_acc+'|'+card_action+'|'+c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+mailer_address1_acc+'|'+mailer_address2_acc+'|'+mailer_address3_acc+'|'+mailer_address4_acc+'|'+mailer_city_acc+'|'+mailer_state_code_acc+'|'+mailer_postal_code_acc+'|'+mailer_mob_acc+'|'+customer_id_acc+'|'+cr_card_limit+'|'+billing_cycle+'|'+superscript+'|'+print_card_holder_name_acc+'|'+joining_fees+'|'+annual_fees+'|'+str(jdtodatestd(date_acc))
                    # ASSIGNING COURIER
    
                    # assignning awb to primary only
                    # if account_number in account_number_list:
                    with open('config/PINCODE_MASTER.csv', 'r') as pin:
                        routing_codewe = pin.readlines()
                        flag = 0
    
                        routing_code = ''
                        customer_code = ''
                        for line in routing_codewe:
                            pincodedata = line.split(',')
                            if mailer_postal_code_acc != '':
                                # and pincodedata[4]=='BLUEDART':
                                if mailer_postal_code_acc in pincodedata[0]:
                                    flag = 1
    
                                    courier = pincodedata[2].rstrip()
                                    routing_code = pincodedata[1].rstrip()
                                    break
                        if flag == 0:
                            courier = 'Speedpost'
                            routing_code = '921-417'
                            courier = str(courier)
                    pin.close()
    
                    # if card_holder_type_acc == '1':
                    # account_number_list.append(account_number_acc)
                    # print(account_number_list)
                    # if account_number in  account_number_list:
                    if card_holder_type_acc == '1' or (card_holder_type_acc == '0' and account_number_acc not in account_number_list):
                        # row=[]
                        #card_type = 'Primary Card'
                        # account_number_list.append(account_number_acc)
                        if courier == 'BLUEDART':
                            with open('config/BD_AWB_USING.txt', 'r') as bdfin:
                                bdawb1 = bdfin.readlines()
                                awb_number = bdawb1[bd_num].rstrip()
                                bd_num+=1
                                awb_number_bd = bdawb1[bd_num:]
                        elif courier == 'DELHIVERY':
                            with open('config/DL_AWB_USING.txt', 'r') as dlfin:
                                dlawb = dlfin.readlines()
                                awb_number = dlawb[dl_num].rstrip()
                                #print(awb_number)
                                dl_num+=1
                                awb_number_dl = dlawb[dl_num:]
                                #print(awb_number_dl[dl_num])
                        elif courier == 'Speedpost':
                            with open('config/IP_AWB_USING.txt', 'r') as ipfin:
                                ipawb = ipfin.readlines()
                                awb_number = ipawb[ip_num].rstrip()
                                ip_num+=1
                                awb_number_ip = ipawb[ip_num:]
    
                    elif card_holder_type_acc == '0' and account_number_acc in account_number_list:
                        #index=np.where(arr == 15)
                        pos = account_number_list.index(account_number_acc)
                        awb_number = account_number_list[pos+1]
                        #add_on_mask_pan = mask_pan_acc
                    else:
                        awb_number = ''
                        #add_on_mask_pan = ''
                    # if card_holder_type_acc == '1':
    
                    account_number_list.extend([account_number_acc, awb_number])
    
                    # if card_holder_type_acc == '0':
                    # print(account_number)
                    #print(account_number_acc, awb_number, card_holder_type_acc)
                    # if card_holder_type_acc == '1':
    
                    # account_number_list.append(account_number_acc)
                    
                    if c_bin_acc == '466505'  and  logo_acc == '101': 
                        product = 'Altura'
                    elif c_bin_acc == '466505'  and  logo_acc == '102':
                        if gender_code_acc == '0':
                            product = 'AlturaPlusBlue'
                        elif gender_code_acc == '1':
                            product = 'AlturaPlusBlue'
                        elif gender_code_acc == '2':
                            product = 'AlturaPlusRuby'
                    
                    elif c_bin_acc == '465523'  and  logo_acc == '301': 
                        product = 'Vetta'
                    
                    #elif c_bin_acc == '457036'  and  logo_acc == '401': 
                    #    product = 'Zenith'
                    elif c_bin_acc == '457036'  and  logo_acc == '401': 
                        #ADDED on 26052022 as per customer requiement new varient
                        #young indians with pastic id 
                        if plastic_id == '          ':
                            product = 'Zenith'
                        elif plastic_id == '0000000001':
                            product = 'Zenith_CII_Young_Indian'
                    
                    #NEW BIN ADDITION PRODUCT DEFINED
                    elif c_bin_acc == '406977'  and  logo_acc == '501':
                        product = 'AU_BANK_LIT_CREDIT_CARD'
                    
                    elif c_bin_acc == '483976'  and  logo_acc == '601':
                        product = 'Corporate_Reward_Credit Card'
                    elif c_bin_acc == '483976'  and  logo_acc == '602':
                        product = 'Corporate_Credit_Card'
                    elif c_bin_acc == '483976'  and  logo_acc == '603':
                        product = 'Secured_Corporate_Credit_Card'
                    
                    elif c_bin_acc == '483974'  and  logo_acc == '701':
                        product = 'Purchase Reward Credit Card'
                    elif c_bin_acc == '483974'  and  logo_acc == '702':
                        product = 'Purchase Credit Card'
                    elif c_bin_acc == '483974'  and  logo_acc == '703':
                        product = 'Secured_Purchase_Credit_Card'
                    
                    elif c_bin_acc == '483894'  and  logo_acc == '801':
                        product = 'Business_Reward_Credit_Card'
                    elif c_bin_acc == '483894'  and  logo_acc == '802':
                        product = 'Secured Business Credit Card'
                    elif c_bin_acc == '483894'  and  logo_acc == '803':
                        product = 'Business Cashback Credit Card'
    
                    #ADDITONAL DETAIL FOR ADD CARDS
                    ps1 = account_number_acc+'|'+card_type+'|'+mask_pan_acc+'|'+card_action+'|'+c_bin_f_acc+'|'+logo_acc+'|' +gender_code_acc+'|'+varient+'|'+mailer_name_acc
                    
                    
                    with open('xxAUF_FF_MIS_MERGE_'+str(ptime)+'.txt', 'a') as ff_file_accm:
                        date_q = jdtodatestd(date_acc)
                        date_q = str(date_q)
    
                        ff_file_accm.write(file_credit_card_ff_acc+str(awb_number)+'|'+routing_code+'|'+courier+'|'+date_q+'\n')
    
                    ff_file_accm.close()
                    
    
                    ps_list.append(ps)
                    ps1_list.append(ps1)
                    pps_list.append(pps)
    
                    cardnumber_list.append(cardnumber_acc)
                    if ((c_bin_acc == '465523' and card_holder_type_acc=='1') or c_bin_acc == '457036'):
                        if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                            if card_holder_type_acc == '1':
                                pp_cardnumber_acc = pp_cardnumber_acc+'01'
                                primary_card.append(cardnumber_acc)
            
                            if card_holder_type_acc == '0':
                                secondary_card.append(cardnumber_acc)
            
                            if (card_holder_type_acc == '0'):
                                card_count = len(secondary_card)
                                r = (range(2, (card_count+1)))
                                cc = card_count+1
            
                                for j in range(cc+1):
                                    ax = str(j)
                                pp_cardnumber_acc = pp_cardnumber_acc+'0'+ax[0:1]
                    
                    if ((c_bin_acc == '465523' and card_holder_type_acc=='1') or c_bin_acc == '457036'):
                        if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                            pp_cardnumber_acc = pp_dup_check(pp_cardnumber_acc)
                        
                        
                    if ((c_bin_acc == '465523' and card_holder_type_acc=='1') or c_bin_acc == '457036'):
                        if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                            pp_cardnumber_acc = pp_dup_check(pp_cardnumber_acc)
                            pp_count = '1'
                        else:
                            pp_cardnumber_acc="'NA"
                    else:
                        pp_cardnumber_acc="'NA"
                    
                    pp_cardnumber_acc = str(pp_cardnumber_acc)
                    
                   
                    track1_acc = '%PP/'+salutation_acc+'/'+print_card_holder_name_acc+'//''?'
                   
                    track2_acc = ';'+pp_cardnumber_acc+'=' +(pp_exp_date_acc[0:2]+'20'+str(int(pp_exp_date_acc[2:4])+3)) + '?'
                    
                    file_credit_card_ff_acc_2_primary = pp_cardnumber_acc+'|'+'|'+'|' +'|'+ref_number+'|'+str(awb_number) +'|'+courier+'|'+routing_code+'|'
                    
                    file_credit_card_ff_acc_2_addon = pp_cardnumber_acc+'|'+'|'+'|' '|'+ref_number+'|'+str(awb_number) + '|'+courier+'|'+routing_code+'|'
    
                    auf_pp_output = account_number_acc+','+logo_acc+','+mask_pan_acc+',' +card_holder_name_acc.rstrip()+','+card_action+',' +pp_cardnumber_acc+','+str(ptime[0:10])
                    
                    bluedart_courier = ref_number+'|'+mailer_name_acc+'|'+mailer_address1_acc+'|'+mailer_address2_acc+'|'+mailer_address3_acc+'-' + mailer_address4_acc+'|'+mailer_city_acc+'|'+mailer_state_code_acc +'||'+mailer_postal_code_acc+'|' +mailer_mob_acc+'|'+str(awb_number)
                    
                    delhivery_courier = str(awb_number)+'|'+ref_number+'|'+mailer_name_acc+'|'+mailer_city_acc+'|'+mailer_state_code_acc+'||'+mailer_address1_acc+' '+mailer_address2_acc+' '+mailer_address3_acc+' '+mailer_address4_acc+'|'+mailer_postal_code_acc+'|'+mailer_mob_acc+'|' + '50|Prepaid|500|Secure Deliverables|AU Centre, 3rd Floor (Credit Card Division), Sunny Trade Centre, New Atish Market, Jaipur, Rajasthan 302019|302019|AU Small Finance Bank Ltd|AU Small Finance Bank Limited AU Centre, 3rd, 5th, 6th & 7th Floor, Sunny Trade Centre, New Atish Market, Jaipur, Rajasthan  302019|True|True'
                    
                    indianpost_courier = '||'+ref_number+'|'+mailer_city_acc+'|'+mailer_postal_code_acc+'|'+mailer_name_acc+'|'+mailer_address1_acc +'|'+mailer_address2_acc+'|'+mailer_address3_acc+'|' +mailer_address4_acc+'|'+mailer_mob_acc+'||'+str(awb_number)                
                    
                    allocation_data_primary = '|'+account_number_acc+'|'+mask_pan_acc+'|'+print_card_holder_name_acc+'|||||'+pp_cardnumber_acc+'||||'+ref_number+'|' +str(awb_number)+'|'+courier+'|'+routing_code+'|'+card_action+'|1|0|1|'+c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+mailer_address1_acc+'|'+mailer_address2_acc+'|'+mailer_address3_acc+'|' +mailer_address4_acc+'|'+mailer_city_acc+'|'+mailer_state_code_acc+'|'+mailer_postal_code_acc+'|' +mailer_mob_acc+'|'+customer_id_acc+'|'+pp_count+'|'+joining_fees +'|'+annual_fees+'|'+str(jdtodatestd(date_acc))                
                    
                    allocation_data_addon = '|'+account_number_acc+'||'+print_card_holder_name_acc+'|'+mask_pan_acc+'|||||'+pp_cardnumber_acc+'|||'+ref_number+'|'+str(awb_number)+'|'+courier+'|'+routing_code+'|'+card_action+'|0|1|1|'+c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+mailer_address1_acc +'|'+mailer_address2_acc+'|'+mailer_address3_acc+'|'+mailer_address4_acc+'|'+mailer_city_acc+'|'+mailer_state_code_acc+'|' +mailer_postal_code_acc+'|'+mailer_mob_acc+'|'+customer_id_acc+'|' +pp_count+'|'+joining_fees+'|'+annual_fees +    '|'+str(jdtodatestd(date_acc))
                    
                    #pp_ff_mis = '|'+account_number_acc+'|'+ref_number+'|'+mask_pan_acc+'|'+print_card_holder_name_acc+'|'+pp_cardnumber_acc+'|'+ref_number+'|'+str(awb_number)+'|'+courier+'|'+routing_code+'|'+card_action+'|0|1|1|'+c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+mailer_address1_acc +'|'+mailer_address2_acc+'|'+mailer_address3_acc+'|'+mailer_address4_acc+'|'+mailer_city_acc+'|'+mailer_state_code_acc+'|' +mailer_postal_code_acc+'|'+mailer_mob_acc+'|'+customer_id_acc+'|' +pp_count+'|'+joining_fees+'|'+annual_fees +    '|'+str(jdtodatestd(date_acc))
                    
                    #if ((c_bin_acc == '465523' and card_holder_type_acc=='1') or c_bin_acc == '457036'):
                    #    if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                    #        allocation_data_primary = '|'+account_number_acc+'|'+mask_pan_acc+'|'+print_card_holder_name_acc+'|||||'+pp_cardnumber_acc+'||||'+ref_number+'|' +str(awb_number)+'|'+courier+'|'+routing_code+'|'+card_action+'|1|0|1|'+c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+mailer_address1_acc+'|'+mailer_address2_acc+'|'+mailer_address3_acc+'|' +mailer_address4_acc+'|'+mailer_city_acc+'|'+mailer_state_code_acc+'|'+mailer_postal_code_acc+'|' +mailer_mob_acc+'|'+customer_id_acc+'|'+'1'+'|'+joining_fees +'|'+annual_fees+'|'+str(jdtodatestd(date_acc))                
                    #        allocation_data_addon = '|'+account_number_acc+'||'+print_card_holder_name_acc+'|'+mask_pan_acc+'|||||'+pp_cardnumber_acc+'|||'+ref_number+'|'+str(awb_number)+'|'+courier+'|'+routing_code+'|'+card_action+'|0|1|1|'+c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+mailer_address1_acc +'|'+mailer_address2_acc+'|'+mailer_address3_acc+'|'+mailer_address4_acc+'|'+mailer_city_acc+'|'+mailer_state_code_acc+'|' +mailer_postal_code_acc+'|'+mailer_mob_acc+'|'+customer_id_acc+'|' +'1'+'|'+joining_fees+'|'+annual_fees +    '|'+str(jdtodatestd(date_acc))
                    #else:
                    #    allocation_data_primary = '|'+account_number_acc+'|'+mask_pan_acc+'|'+print_card_holder_name_acc+'|||||'+''+'||||'+ref_number+'|' +str(awb_number)+'|'+courier+'|'+routing_code+'|'+card_action+'|1|0|1|'+c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+mailer_address1_acc+'|'+mailer_address2_acc+'|'+mailer_address3_acc+'|' +mailer_address4_acc+'|'+mailer_city_acc+'|'+mailer_state_code_acc+'|'+mailer_postal_code_acc+'|' +mailer_mob_acc+'|'+customer_id_acc+'|'+'1'+'|'+joining_fees +'|'+annual_fees+'|'+str(jdtodatestd(date_acc))                
                    #    allocation_data_addon = '|'+account_number_acc+'||'+print_card_holder_name_acc+'|'+mask_pan_acc+'|||||'+''+'|||'+ref_number+'|'+str(awb_number)+'|'+courier+'|'+routing_code+'|'+card_action+'|0|1|1|'+c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+mailer_address1_acc +'|'+mailer_address2_acc+'|'+mailer_address3_acc+'|'+mailer_address4_acc+'|'+mailer_city_acc+'|'+mailer_state_code_acc+'|' +mailer_postal_code_acc+'|'+mailer_mob_acc+'|'+customer_id_acc+'|' +'1'+'|'+joining_fees+'|'+annual_fees +    '|'+str(jdtodatestd(date_acc))
                        
                            
                    if ((c_bin_acc == '465523' and card_holder_type_acc=='1') or c_bin_acc == '457036'):
                        if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                            if mask_pan_acc not in filecontents:
                                file_pp = '#0#'+mask_pan_acc+'#1#'+pp_cardnumber_acc+'#2#'+track1_acc+'#3#'+track2_acc +'#4#'+ (pp_exp_date_acc[0:2]+'/'+str(int(pp_exp_date_acc[2:4])+3)) +'#5#'+salutation_acc +' '+print_card_holder_name_acc+'#6#'
                                
                                file_pp_merge = account_number_acc+'|'+ref_number+'|'+mask_pan_acc+'|'+salutation_acc+' ' +print_card_holder_name_acc+'|'+pp_cardnumber_acc+'|' + (pp_exp_date_acc[0:2]+'/'+str(int(pp_exp_date_acc[2:4])+3)) +'|'+varient+'|'+logo_acc+'|'+gender_code_acc
    
                    if courier == 'Speedpost':
                        with open('xxxAUF_Credit_IndiaPost_Courier_Connection_Report_.txt', 'a') as ff_ip_acc:
                            # ff_ip_acc.write(indianpost_courier_1+indianpost_courier_2+'\n')
                            ff_ip_acc.write(indianpost_courier+'\n')
                        ff_ip_acc.close()
                    elif courier == 'DELHIVERY':
                        with open('xxxAUF_Credit_Delhivery_Courier_Connection_Report_.txt', 'a') as ff_dl_acc:
                            ff_dl_acc.write(delhivery_courier+'\n')
                        ff_dl_acc.close()
                    elif courier == 'BLUEDART':
                        with open('xxxAUF_Credit_Bluedart_Courier_Connection_Report_.txt', 'a') as ff_bd_acc:
                            ff_bd_acc.write(bluedart_courier+'\n')
                        ff_bd_acc.close()
                    
                    
                    if ((card_holder_type_acc == '1') and (card_action_code=='3' or card_action_code== 'L')):
                        with open('xxAUF_Replace_FF_MIS_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+str(product).replace('AU_BANK_LIT_CREDIT_CARD','Lit_Credit_Card')+'_'+celeb+'.txt', 'a') as ff_file_acc:
                            ff_file_acc.write(file_credit_card_ff_acc_primary +file_credit_card_ff_acc_2_primary+file_credit_card_ff_acc_3_primary_replace+'\n')
                        ff_file_acc.close()
                        with open('xxAUC_EM_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+str(product).replace('AU_BANK_LIT_CREDIT_CARD','Lit_Credit_Card')+'_'+celeb+'_Pri_Replace.txt', 'a') as em_file_acc:
                            em_file_acc.write(file_credit_card_em_acc+courier+'\n')
                        em_file_acc.close()
                    elif ((card_holder_type_acc == '0') and (card_action_code=='3' or card_action_code== 'L')):
                        with open('xxAUF_Replace_FF_MIS_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+str(product).replace('AU_BANK_LIT_CREDIT_CARD','Lit_Credit_Card')+'_'+celeb+' - Add-On-Card.txt', 'a') as ff_addonfile_acc:
                            ff_addonfile_acc.write(file_credit_card_ff_acc_addon+file_credit_card_ff_acc_2_addon+file_credit_card_ff_acc_3_addon_replace+'\n')
                        ff_addonfile_acc.close()
                        with open('xxAUC_EM_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+str(product).replace('AU_BANK_LIT_CREDIT_CARD','Lit_Credit_Card')+'_'+celeb+'_AddOn_Replace.txt', 'a') as em_file_acc:
                            em_file_acc.write(file_credit_card_em_acc+courier+'\n')
                        em_file_acc.close()
                    elif card_holder_type_acc == '1' :
                        with open('xxAUF_FF_MIS_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+str(product).replace('AU_BANK_LIT_CREDIT_CARD','Lit_Credit_Card')+'_'+celeb+'.txt', 'a') as ff_file_acc:
                            ff_file_acc.write(file_credit_card_ff_acc_primary +file_credit_card_ff_acc_2_primary+file_credit_card_ff_acc_3_primary+'\n')
                        ff_file_acc.close()
                        with open('xxAUC_EM_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+str(product).replace('AU_BANK_LIT_CREDIT_CARD','Lit_Credit_Card')+'_'+celeb+'_Pri.txt', 'a') as em_file_acc:
                            em_file_acc.write(file_credit_card_em_acc+courier+'\n')
                        em_file_acc.close()
                    elif card_holder_type_acc == '0':
                        with open('xxAUF_FF_MIS_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+str(product).replace('AU_BANK_LIT_CREDIT_CARD','Lit_Credit_Card')+'_'+celeb+' - Add-On-Card.txt', 'a') as ff_addonfile_acc:
                            ff_addonfile_acc.write(file_credit_card_ff_acc_addon+file_credit_card_ff_acc_2_addon+file_credit_card_ff_acc_3_addon+'\n')
                        ff_addonfile_acc.close()
                        with open('xxAUC_EM_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+str(product).replace('AU_BANK_LIT_CREDIT_CARD','Lit_Credit_Card')+'_'+celeb+'_Add.txt', 'a') as em_file_acc:
                            em_file_acc.write(file_credit_card_em_acc+courier+'\n')
                        em_file_acc.close()
    
    
                    ##############################################################
                    '''  
                    with open('xxAUF_Credit_Data_Allocation_Report_.txt', 'a') as ff_file_acc:
                        ff_file_acc.write(allocation_data_primary+'\n')
                    ff_file_acc.close()
                    # with open('xxAUF_FF_MIS_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+str(product)+'_'+celeb+'_'+str(ptime)+'.txt', 'a') as ff_file_acc:
                    COMMENTED FOR REPLACE CARDS DIFFRENTIATON
                    if (card_holder_type_acc == '1'):
                        with open('xxAUF_FF_MIS_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+str(product)+'_'+celeb+'.txt', 'a') as ff_file_acc:
                            ff_file_acc.write(file_credit_card_ff_acc_primary +
                                              file_credit_card_ff_acc_2_primary+file_credit_card_ff_acc_3_primary+'\n')
                        ff_file_acc.close()
                        with open('xxAUC_EM_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+str(product)+'_'+celeb+'_pri.txt', 'a') as em_file_acc:
                            em_file_acc.write(file_credit_card_em_acc+courier+'\n')
                        em_file_acc.close()
                    elif card_holder_type_acc == '0':
                        with open('xxAUF_FF_MIS_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+str(product)+'_'+celeb+' - Add-On-Card.txt', 'a') as ff_addonfile_acc:
                            ff_addonfile_acc.write(
                                file_credit_card_ff_acc_addon+file_credit_card_ff_acc_2_addon+file_credit_card_ff_acc_3_addon+'\n')
                        ff_addonfile_acc.close()
                        with open('xxAUC_EM_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+str(product)+'_'+celeb+'_add.txt', 'a') as em_file_acc:
                            em_file_acc.write(file_credit_card_em_acc+courier+'\n')
                        em_file_acc.close()
    
                    with open('xxAUF_Credit_Data_Allocation_Report_.txt', 'a') as ff_file_acc:
                        ff_file_acc.write(allocation_data_primary+'\n')
                    ff_file_acc.close()
                    
                    #####################################################
                    #REMOVING PP CARDS FOR ADD OF VETTA
                    #####################################################
                    if (c_bin_acc == '465523' or c_bin_acc == '457036'):
                        if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                            if mask_pan_acc not in filecontents:
                                with open('AUC_PP_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+product+'_'+str(ptime)+'EM.txtt', 'a') as pp_file:
                                    pp_file.write(file_pp + '\n')
                                    #print (file_pp)
                                pp_file.close()
    
                    if (c_bin_acc == '465523' or c_bin_acc == '457036'):
                        if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                            if mask_pan_acc not in filecontents:
                                with open('xxAUC_PP_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+product+'_'+str(ptime)+'.csv', 'a') as pp_file:
                                    pp_file.write('Sr. No|Account Number|Ref no.|Primary Card number|Customer Name|PP  Card No_Primary|Expiry Date|Variant|Logo|Gender|AWB. No.|Courier\n')
                                    pp_file.write(file_credit_card_ff_acc_new+'|' + str(awb_number)+'|'+courier+'|'+routing_code+'\n')
                                    count += 1
                                pp_file.close()
    
                    if (c_bin_acc == '465523' or c_bin_acc == '457036'):
                        if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                            if mask_pan_acc not in filecontents:
                                with open('AUC_PP_MERGE_'+str(ptime)+'.dat', 'a') as pp_file_m:
                                    pp_file_m.write(file_pp_merge + '\n')
                                pp_file_m.close()
    
                    if (c_bin_acc == '465523' or c_bin_acc == '457036'):
                        if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                            if mask_pan_acc not in filecontents:
                                with open('Priority_Pass_Data_'+str(ptime[0:10])+'.csv', 'a') as pp_file_auf:
                                    if count == 0:
                                        pp_file_auf.write('')
    
                                    pp_file_auf.write(auf_pp_output + '\n')
    
                                pp_file_auf.close()
                    '''
                    #comneted for replace cards
                    
                    if card_holder_type_acc == '1':
                        with open('xxAUF_Credit_Data_Allocation_Report_.txt', 'a') as ff_file_acc:
                            ff_file_acc.write(allocation_data_primary+'\n')
                        ff_file_acc.close()
                    elif card_holder_type_acc == '0':
                        with open('xxAUF_Credit_Data_Allocation_Report_.txt', 'a') as ff_file_acc:
                            ff_file_acc.write(allocation_data_addon+'\n')
                        ff_file_acc.close()
                    
                   
                    if ((c_bin_acc == '465523' and card_holder_type_acc=='1') or c_bin_acc == '457036'):
                        if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                            if mask_pan_acc not in filecontents:
                                with open('xxAUC_PP_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+str(product).replace('AU_BANK_LIT_CREDIT_CARD','Lit_Credit_Card')+'_'+'EM.txt', 'a') as pp_file:
                                    pp_file.write(file_pp+courier[0:1] + '\n')
                                    #print (file_pp)
                                pp_file.close()
                    
                    if ((c_bin_acc == '465523' and card_holder_type_acc=='1') or c_bin_acc == '457036'):
                        if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                            if mask_pan_acc not in filecontents:
                                with open('xxAUC_PP_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+str(product).replace('AU_BANK_LIT_CREDIT_CARD','Lit_Credit_Card')+'_MIS.txt', 'a') as pp_file:
                                    pp_file.write('|' +file_pp_merge+'|' +awb_number+'|'+courier+ '\n')
                                    #print (file_pp)
                                pp_file.close()
    
                   
                    if ((c_bin_acc == '465523' and card_holder_type_acc=='1') or c_bin_acc == '457036'):
                        if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                            if mask_pan_acc not in filecontents:
                                with open('AUC_PP_MERGE_'+str(ptime)+'.dat', 'a') as pp_file_m:
                                    pp_file_m.write(file_pp_merge + '\n')
                                    total_pp_count+=1
                                pp_file_m.close()
    
                    if ((c_bin_acc == '465523' and card_holder_type_acc=='1') or c_bin_acc == '457036'):
                        if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                            if mask_pan_acc not in filecontents:
                                with open('Priority_Pass_Data_'+str(ptime[0:10])+'.csv', 'a') as pp_file_auf:
                                    if count == 0:
                                        pp_file_auf.write('')
                                    pp_file_auf.write(auf_pp_output + '\n')
                                pp_file_auf.close()
                    
                    #Alert for new bin -483974
                    if (c_bin_acc == '483974' ):
                        with open('ALERT!!___NEW BIN 483974 RECEIVED.dat', 'a') as alert_ff:
                            alert_ff.write(c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+ref_number+'|'+card_type+'|'+mask_pan_acc+'|'+account_number_acc+'|'+card_action+'\n')
                        alert_ff.close()
                                
                                
        #print(len(awb_number_bd))
        if len(awb_number_bd)>0:#if awb not used then all awb reverted
            with open('config/BD_AWB_USING.txt', 'w') as bdfout:
                bdfout.writelines(awb_number_bd)
        if len(awb_number_dl)>0:#if awb not used then all awb reverted
            with open('config/DL_AWB_USING.txt', 'w') as dlfout:
                dlfout.writelines(awb_number_dl)
        if len(awb_number_ip)>0:#if awb not used then all awb reverted
            with open('config/IP_AWB_USING.txt', 'w') as ipfout:
                ipfout.writelines(awb_number_ip)
        
        #print(account_number_list)
    
    outfile_acc.close()
    
    del_file2 = glob.glob("*account*")
    for del2 in del_file2:
        os.remove(del2)
    
    print("\nEMBO and MIS files generated.....")
    print("\nSorting and excel conversion begins.....")
    for idx, val in enumerate(ps_list):
        #print(idx, val)
        acc_card_count = (ps_list.count(ps_list[idx]))
        if ps_list[idx][17:] == 'Primary Card':
            p_acc_card_count.append(
                str(ps_list[idx])+'|'+str(ps_list.count(ps_list[idx])))
        if ps_list[idx][17:] == 'Add-on  Card':
            s_acc_card_count.append(
                str(ps_list[idx])+'|'+str(ps_list.count(ps_list[idx])))
    
    with open('PrimaryCard_detail_'+str(ptime)+'.dat', 'w') as ps_d:
        ps_d.writelines(["%s\n" % item for item in p_acc_card_count])
    ps_d.close()
    
    
    with open('del_SecondaryCard.txt', 'w') as ps_d:
        ps_d.writelines(["%s\n" % item for item in s_acc_card_count])
        # for oni in s_acc_card_count:
        # print ((oni))
    ps_d.close()
    
    uniqlines = set(open('del_SecondaryCard.txt').readlines())
    bar = open('SecondaryCard_details_'+str(ptime) +'.dat', 'w').writelines(set(uniqlines))
    
    for idx, val in enumerate(ps1_list):
        #print(idx, val)
        acc_card_count1 = (ps1_list.count(ps1_list[idx]))
        # if ps_list[idx][17:] == 'Primary Card':
        # p_acc_card_count.append(str(ps_list[idx])+'|'+str(ps_list.count(ps_list[idx])))
        if ps_list[idx][17:29] == 'Add-on  Card':
            s_acc_card_count1.append(
                str(ps1_list[idx])+'|'+str(ps1_list.count(ps1_list[idx])))
    '''
    with open('PrimaryCard_detail_'+str(ptime)+'.txt', 'w') as ps_d:
      ps_d.writelines(["%s\n" % item  for item in p_acc_card_count])
    ps_d.close()
    '''
    
    with open('del_SecondaryCard1.txt', 'w') as ps_d:
        ps_d.writelines(["%s\n" % item for item in s_acc_card_count1])
        # for oni in s_acc_card_count1:
        #print ((oni))
    ps_d.close()
    
    uniqlines = set(open('del_SecondaryCard1.txt').readlines())
    bar = open('SecondaryCard1_details_'+str(ptime) +
               '.txt', 'w').writelines(set(uniqlines))
    
    
    
    
    def excel_convertor(name_ff):
        #ext='.txt'
        if Path(name_ff).is_file():
            #print('file present')
            records_list = []
            s_no = 0
            with open(name_ff, "r") as ff, open(name_ff[2:], "w") as foutfile:
                foutfile.write("Sr. No|Account Number|Primary Card number|Customer Name|Add-on Card 1|Add-on Card 2|Add-on Card 3|Add-on Card 4|PP  Card No_Primary|PP  Card No_Addon1|PP  Card No_Addon2|PP  Card No_Addon3|Ref no.|AWB. No.|Courier|Courier Code|Card Action|Primary Count|Add-on Count|Total Cards|Bin|Logo|Gender Code|Varient|Address Line 1|Address Line 2|Address Line 3|Address Line 4|City|State Code|Postal Code|Mobile Number|Cust Unique ID|Credit Limit|Statement Date |Extention|Embo_Name|Joining Fees|Annual Fees|Card Issuance Date"+'\n')
                contents = ff.readlines()
                # sorting using our custom logic
                contents.sort(key=my_sort_ff)
                for fi in contents:
                    records_list.append(fi)
                    s_no = (records_list.index(fi)+1)
                    s_no = "%05d" % s_no
                    if not fi.strip():
                        continue
                    if fi:
                        foutfile.write(str(s_no)+fi)
            ff.close()
            foutfile.close()
            df = pd.read_csv(name_ff[2:],encoding= 'unicode_escape', sep='|', dtype=object)
            df.to_excel(name_ff[2:-4]+'_'+ str(s_no)+'.xlsx', 'Sheet1', index=False) 
            
            os.remove(name_ff)
            os.remove(name_ff[2:])
            
    def excel_convertor_replace(name_ff):
        #ext='.txt'
        if Path(name_ff).is_file():
            #print('file present')
            records_list = []
            s_no = 0
            with open(name_ff, "r") as ff, open(name_ff[2:], "w") as foutfile:
                foutfile.write("Sr. No|Account Number|Primary Card number|Customer Name|Add-on Card 1|Add-on Card 2|Add-on Card 3|Add-on Card 4|PP  Card No_Primary|PP  Card No_Addon1|PP  Card No_Addon2|PP  Card No_Addon3|Ref no.|AWB. No.|Courier|Courier Code|Card Action|Primary Count|Add-on Count|Total Cards|Bin|Logo|Gender Code|Varient|Address Line 1|Address Line 2|Address Line 3|Address Line 4|City|State Code|Postal Code|Mobile Number|Cust Unique ID|Credit Limit|Statement Date |Extention|Embo_Name"+'\n')
                contents = ff.readlines()
                # sorting using our custom logic
                contents.sort(key=my_sort_ff)
                for fi in contents:
                    records_list.append(fi)
                    s_no = (records_list.index(fi)+1)
                    s_no = "%05d" % s_no
                    if not fi.strip():
                        continue
                    if fi:
                        foutfile.write(str(s_no)+fi)
            ff.close()
            foutfile.close()
            df = pd.read_csv(name_ff[2:],encoding= 'unicode_escape', sep='|', dtype=object)
            df.to_excel(name_ff[2:-4]+'_'+ str(s_no)+'.xlsx', 'Sheet1', index=False) 
            
            os.remove(name_ff)
            os.remove(name_ff[2:])
            
    
    def embo_convertor(name_embo):
        #ext='.txt'
        if Path(name_embo).is_file():
            with open(name_embo, "r") as bf, open(name_embo[2:-4]+'_'+str(ptime)+'.txtt', "w") as boutfile:
                contents = bf.readlines()
                # sorting using our custom logic
                contents.sort(key=my_sort_emb)
                for bi in contents:
                    if not bi.strip():
                        continue
                    if bi:
                        boutfile.write(bi)
                        #total_primary_count+=1
            bf.close()
            boutfile.close()
        os.remove(name_embo)
        
    def pp_embo_convertor(pp_name_embo):
        if Path(pp_name_embo).is_file():  
            with open(pp_name_embo, "r") as bf, open(pp_name_embo[2:-4]+str(ptime)+'.txtt', "w") as boutfile:
                    contents = bf.readlines()
                    # sorting using our custom logic
                    contents.sort(key=pp_sort_emb)
                    for bi in contents:
                        if not bi.strip():
                            continue
                        if bi:
                            boutfile.write(bi)
                            #total_pp_count+=1
            bf.close()
            boutfile.close()
        os.remove(pp_name_embo)
        
        
    def pp_excel_convertor(pp_name_ff):
        #ext='.txt'
        if Path(pp_name_ff).is_file():
            #print('file present')
            records_list = []
            s_no = 0  
            with open(pp_name_ff, "r") as ff, open(pp_name_ff[2:], "w") as foutfile:
                foutfile.write('Sr. No|Account Number|Ref no.|Primary Card number|Customer Name|PP  Card No_Primary|Expiry Date|Variant|Logo|Gender|AWB. No.|Courier'+'\n')
                contents = ff.readlines()
                # sorting using our custom logic
                contents.sort(key=my_sort_pp)
                for fi in contents:
                    records_list.append(fi)
                    s_no = (records_list.index(fi)+1)
                    s_no = "%05d" % s_no
                    if not fi.strip():
                        continue
                    if fi:
                        foutfile.write(str(s_no)+fi)
            ff.close()
            foutfile.close()
            df = pd.read_csv(pp_name_ff[2:],encoding= 'unicode_escape', sep='|', dtype=object)
            df.to_excel(pp_name_ff[2:-4]+ '_'+str(s_no)+'.xlsx', 'Sheet1', index=False) 
            
            os.remove(pp_name_ff)
            os.remove(pp_name_ff[2:])
            #os.remove(name_embo+ext)
    
    
    ff_filename = glob.glob("xxAUF_FF_MIS_B*")
    #print('File names:', ff_filename)
    for file in ff_filename:
        excel_convertor(file)
    
    
    ff_filename = glob.glob("xxAUF_Replace_FF_MIS_B*")
    #print('File names:', ff_filename)
    for file in ff_filename:
        excel_convertor_replace(file)
    
    
    
    
    embo_filename = glob.glob("xxAUC_EM_B*")
    #print('File names:', embo_filename)
    for file in embo_filename:
        embo_convertor(file)
    
    
    pp_embo_filename = glob.glob("xxAUC_PP_B*_EM.txt")
    #print('File names:', embo_filename)
    for file in pp_embo_filename:
        pp_embo_convertor(file)
    
    pp_mis_filename = glob.glob("xxAUC_PP_B*_MIS.txt")
    #print('File names:', embo_filename)
    for file in pp_mis_filename:
        pp_excel_convertor(file)
        
    
    '''
    pp_name1 = 'xxAUC_PP_B457036_L401_G1_Zenith_MIS'
    pp_embo_name1 = 'xxAUC_PP_B457036_L401_G1_Zenith_EM'
    pp_excel_convertor(pp_name1,pp_embo_name1)
        
    pp_name2 = 'xxAUC_PP_B457036_L401_G2_Zenith_MIS'
    pp_embo_name2 = 'xxAUC_PP_B457036_L401_G2_Zenith_EM'
    pp_excel_convertor(pp_name2,pp_embo_name2)
        
    pp_name3 = 'xxAUC_PP_B465523_L301_G1_Vetta_MIS'
    pp_embo_name3 = 'xxAUC_PP_B465523_L301_G1_Vetta_EM'
    pp_excel_convertor(pp_name3,pp_embo_name3)
        
    pp_name4 = 'xxAUC_PP_B465523_L301_G2_Vetta_MIS'
    pp_embo_name4 = 'xxAUC_PP_B465523_L301_G2_Vetta_EM'
    pp_excel_convertor(pp_name4,pp_embo_name4)
    
    '''
    print("\nSorting and Excel Converted.....")
    print("\nCourier connection reports generating.....")
    IndiaPost_Courier = 'xxxAUF_Credit_IndiaPost_Courier_Connection_Report_.txt'
    if Path(IndiaPost_Courier).is_file():
        records_list = []
        s_no = 0
        with open('xxxAUF_Credit_IndiaPost_Courier_Connection_Report_.txt', "r") as ff, open('AUF_Credit_IndiaPost_Courier_Connection_Report_.txt', "w") as foutfile:
            foutfile.write('SNO|Barcode_Value|REFERANCE NUMBER|CITY|PINCODE|NAME|ADDRESS 1|ADDRESS 2|ADDRESS 3|ADDRESSEE EMAIL|ADDRESSEE MOBILE|SENDER MOBILE|POD REQUIRED'+'\n')
            contents = ff.readlines()
            # sorting using our custom logic
            # contents.sort(key=my_sort_ff)
            for fi in contents:
                records_list.append(fi)
                s_no = (records_list.index(fi)+1)
                s_no = "%05d" % s_no
                if not fi.strip():
                    continue
                if fi:
                    foutfile.write(str(s_no)+fi)
        ff.close()
        foutfile.close()
        df = pd.read_csv('AUF_Credit_IndiaPost_Courier_Connection_Report_.txt',encoding= 'unicode_escape', sep='|', dtype=object)
        df.to_excel('AUF_Credit_IndiaPost_Courier_Connection_Report_' +str(s_no)+'_'+str(ptime)+'.xlsx', 'Sheet1', index=False)
        os.remove('xxxAUF_Credit_IndiaPost_Courier_Connection_Report_.txt')
        os.remove('AUF_Credit_IndiaPost_Courier_Connection_Report_.txt')
    
    Delhivery_Courier = 'xxxAUF_Credit_Delhivery_Courier_Connection_Report_.txt'
    if Path(Delhivery_Courier).is_file():
        records_list=[]
        s_no=0
        with open('xxxAUF_Credit_Delhivery_Courier_Connection_Report_.txt',"r") as ff, open('AUF_Credit_Delhivery_Courier_Connection_Report_.txt',"w") as foutfile:
            foutfile.write('Waybill|Order No/Reference No|Consignee Name|City|State|Country|Address|Pincode|Phone/Mobile|Weight|Payment Mode|Package Amount|Product to be Shipped|Return Address|Return Pin|Seller Name|Seller Address|person_specific|address_specific'+'\n')
            contents = ff.readlines()
            for fi in contents:
                records_list.append(fi)
                s_no= (records_list.index(fi)+1)
                s_no = "%05d" % s_no
                if not fi.strip():
                    continue
                if fi:
                    foutfile.write(fi)
        ff.close()
        foutfile.close()
        
    
        df = pd.read_csv('AUF_Credit_Delhivery_Courier_Connection_Report_.txt',encoding= 'unicode_escape', sep='|', dtype=object)
        df.to_excel('AUF_Credit_Delhivery_Courier_Connection_Report_'+str(s_no)+'_'+str(ptime)+'.xlsx', 'Sheet1',index=False)
        os.remove('xxxAUF_Credit_Delhivery_Courier_Connection_Report_.txt')
        os.remove('AUF_Credit_Delhivery_Courier_Connection_Report_.txt')
    
    Bluedart_Courier = 'xxxAUF_Credit_Bluedart_Courier_Connection_Report_.txt'
    if Path(Bluedart_Courier).is_file():
        records_list = []
        s_no = 0
        with open('xxxAUF_Credit_Bluedart_Courier_Connection_Report_.txt', "r") as ff, open('AUF_Credit_Bluedart_Courier_Connection_Report_.txt', "w") as foutfile:
            foutfile.write(
                'Refrence Nuumber|Customer Name|ADDRESS1|ADDRESS2|ADDRESS3|CITY|STATE|COUNTRY|PINCODE|CONTACT1|AWB'+'\n')
            contents = ff.readlines()
            for fi in contents:
                records_list.append(fi)
                s_no = (records_list.index(fi)+1)
                s_no = "%05d" % s_no
                if not fi.strip():
                    continue
                if fi:
                    foutfile.write(fi)
        ff.close()
        foutfile.close()
        df = pd.read_csv('AUF_Credit_Bluedart_Courier_Connection_Report_.txt',encoding= 'unicode_escape', sep='|', dtype=object)
        df.to_excel('AUF_Credit_Bluedart_Courier_Connection_Report_' +str(s_no)+'_'+str(ptime)+'.xlsx', 'Sheet1', index=False)
        os.remove('xxxAUF_Credit_Bluedart_Courier_Connection_Report_.txt')
        os.remove('AUF_Credit_Bluedart_Courier_Connection_Report_.txt')
    
    with open('xxAUF_FF_MIS_MERGE_'+str(ptime)+'.txt', "r") as ff, open('AUF_FF_MIS_MERGE_'+str(ptime)+'.txt', "w") as foutfile:
        records_list = []
        s_no = 0
        foutfile.write("Sr. No|FIRST SIX|Logo|Gender Code|Varient|Ref no.|CARD TYPE|MASK PAN|ACC NO|CARD ACTION|SALUTATION|MAILER NAME|Address Line 1|Address Line 2|Address Line 3|Address Line 4|City|State Code|Postal Code|Mobile Number|Cust Unique ID|Credit Limit|Statement Date |Extention|Embo_Name|PCT ID|AWB. No.|ROUTING CODE|Courier|Card Issuance Date"+'\n')
        contents = ff.readlines()
        # sorting using our custom logic
        # contents.sort(key=my_sort_ff)
        for fi in contents:
            records_list.append(fi)
            s_no = (records_list.index(fi)+1)
            s_no = "%05d" % s_no
            if not fi.strip():
                continue
            if fi:
                foutfile.write(str(s_no)+fi)
        total_primary_count = s_no
    ff.close()
    foutfile.close()
    df = pd.read_csv('AUF_FF_MIS_MERGE_'+str(ptime)+'.txt',encoding= 'unicode_escape', sep='|', dtype=object)
    df.to_excel('AUF_FF_MIS_MERGE_'+str(ptime)+'-' +str(s_no)+'.xlsx', 'Sheet1', index=False)
    os.remove('xxAUF_FF_MIS_MERGE_'+str(ptime)+'.txt')
    os.remove('AUF_FF_MIS_MERGE_'+str(ptime)+'.txt')
    
    
    with open('xxAUF_Credit_Data_Allocation_Report_.txt', "r") as ff, open('AUF_Credit_Data_Allocation_Report_.txt', "w") as foutfile:
        records_list = []
        s_no = 0
        foutfile.write('Sr. No|Account Number|Primary Card number|Customer Name|Add-on Card 1|Add-on Card 2|Add-on Card 3|Add-on Card 4|PP  Card No_Primary|PP  Card No_Addon1|PP  Card No_Addon2|PP  Card No_Addon3|Ref no.|AWB. No.|Courier|Courier Code|Card Action|Primary Count|Add-on Count|Total Cards|Bin|Logo|Gender Code|Varient|Address Line 1|Address Line 2|Address Line 3|Address Line 4|City|State Code|Postal Code|Mobile Number|Cust Unique ID|Total PP Count|Joining Fees|Annual Fees|Card Issuance Date'+'\n')
        contents = ff.readlines()
        for fi in contents:
            records_list.append(fi)
            s_no = (records_list.index(fi)+1)
            s_no = "%05d" % s_no
            if not fi.strip():
                continue
            if fi:
                foutfile.write(s_no+fi)
    ff.close()
    foutfile.close()
    df = pd.read_csv('AUF_Credit_Data_Allocation_Report_.txt',encoding= 'unicode_escape',sep='|', dtype=object)
    df.to_excel('AUF_Credit_Data_Allocation_Report_'+str(s_no) +'_'+str(total_pp_count) +'_'+str(ptime)+'.xlsx', 'Sheet1', index=False)
    os.remove('xxAUF_Credit_Data_Allocation_Report_.txt')
    os.remove('AUF_Credit_Data_Allocation_Report_.txt')
    
    
    '''
    #del_file1 = glob.glob("del*")
    #for de in del_file1:
    #    os.remove(de)
    
    #del_file2 = glob.glob("*account*")
    #for del2 in del_file2:
    #    os.remove(del2)
    
    
    
    
    #del_file1 = glob.glob("*.txt")
    #for de in del_file1:
    #    os.remove(de)
    '''
    
    del_file = glob.glob("L2CDZU*")
    for dem in del_file:
        os.remove(dem)
    del_file = glob.glob("merge*")
    for dem in del_file:
        os.remove(dem)
    del_file1 = glob.glob("del*")
    for de in del_file1:
        os.remove(de)
    
    
    print("\nCourier connection reports generated.....")
    print("\nBatch Card generating.....")
    
        
    for i,k in enumerate(file_name):
        result = hashlib.md5(file_name[i].encode())
        filenamehash = result.hexdigest()
        filenamehash = str(filenamehash)
        #print (file_name[i]+'---'+filenamehash)
        with open('C:/AUTO-PROCESS-CONFIG/AUC/AUC_PROCESSING_'+str(ptime)+'.log', 'a') as hashfile:
            hashfile.write("File Processed  ")
            hashfile.write(file_name[i]+'|'+str(ptime)+'|'+filenamehash+'  ')
            hashfile.write("File Deleted \n")
        hashfile.close()
        with open('C:/AUTO-PROCESS-CONFIG/AUC/AUC_PROCESSING.log', 'a') as hashfilem:
            hashfilem.write("File Processed  ")
            hashfilem.write(file_name[i]+'|'+str(ptime)+'|'+filenamehash+'  ')
            hashfilem.write("File Deleted \n")
        hashfilem.close()
             
    file_count = '.'
    
    
    os.chdir(file_count)
    names={}
    for fn in glob.glob('*AUC*.txtt'):
        with open(fn) as f:
            names[fn]=sum(1 for file_count in f if file_count.strip() and not file_count.startswith('~'))       
    with open('AUF_FILE_COUNT_'+str(ptime)+'.csv', 'w') as f:
        f.write('File Name,File Count,Non-Replace,Replace'+'\n')
        [f.write('{0},{1}\n'.format(key, value)) for key, value in names.items()] 
    
    from prettytable import PrettyTable
    ptx = PrettyTable()
    ptx.field_names = ["Bin", "Artwork No.","JB No.", "EMBOSS Filename","Qty", "Job setup", "Method -Ribbon/Foil"]
    
    for key, value in names.items():
        if key[23:46] == 'Zenith_CII_Young_Indian':
            art_work = 'V00884'
            job_setup = 'AUF_CR_VISA_457036_DI'
            dg_color = 'DG-White'
        elif key[4:19] == 'EM_B457036_L401':
            art_work = 'V00706'
            job_setup = 'AUF_CR_VISA_457036_DI'
            dg_color = 'DG-White'
        elif key[4:19] == 'EM_B406977_L501':
            art_work = 'V00937'
            job_setup = 'AUF_CR_VISA_406977_INFINEON'
            dg_color = 'DG-Black'
        elif key[4:19] == 'EM_B465523_L301':
            art_work = 'V00707'
            job_setup = 'AUF_CR_VISA_465523_DI'
            dg_color = 'DG-White'
        #===========ADDED ON 26-05-2022===========================
        elif key[4:18] == 'EM_B483974_L70':
            art_work = 'V00875'
            job_setup = 'AUF_CR_VISA_483974_DI'
            dg_color = 'DG-White'
    
        elif key[4:18] == 'EM_B483976_L60':
            art_work = 'V00874'
            job_setup = 'AUF_CR_VISA_483976_DI'
            dg_color = 'DG-White'
            
        elif key[4:18] == 'EM_B483894_L80':
            art_work = 'V00876'
            job_setup = 'AUF_CR_VISA_483894_DI'
            dg_color = 'DG-White'
        #=========================================================
        elif key[0:31] == 'AUC_EM_B466505_L101_G0_Altura__':
            art_work = 'V00703'
            job_setup = 'AUF_CR_VISA_466505_DI'
            dg_color = 'DG-White'
        elif key[0:31] == 'AUC_EM_B466505_L101_G1_Altura__':
            art_work = 'V00703'
            job_setup = 'AUF_CR_VISA_466505_DI'
            dg_color = 'DG-White'
        elif key[0:31] == 'AUC_EM_B466505_L101_G2_Altura__':
            art_work = 'V00703'
            job_setup = 'AUF_CR_VISA_466505_DI'
            dg_color = 'DG-White'
            
        #===========ADDED ON 01-06-2022===========================
        elif key[0:33] == 'AUC_EM_B466505_L101_G0_Altura_C_F':
            art_work = 'V00796'
            job_setup = 'AUF_CR_VISA_466505_Celeb_DI'
            dg_color = 'DG-White'
            
        #=========================================================
        elif key[0:33] == 'AUC_EM_B466505_L101_G1_Altura_C_F':
            art_work = 'V00796'
            job_setup = 'AUF_CR_VISA_466505_Celeb_DI'
            dg_color = 'DG-White'
        elif key[0:33] == 'AUC_EM_B466505_L101_G2_Altura_C_F':
            art_work = 'V00796'
            job_setup = 'AUF_CR_VISA_466505_Celeb_DI'
            dg_color = 'DG-White'
            
        elif key[0:33] == 'AUC_EM_B466505_L101_G0_Altura_C_M':
            art_work = 'V00794'
            job_setup = 'AUF_CR_VISA_466505_Celeb_DI'
            dg_color = 'DG-White'
        elif key[0:33] == 'AUC_EM_B466505_L101_G1_Altura_C_M':
            art_work = 'V00794'
            job_setup = 'AUF_CR_VISA_466505_Celeb_DI'
            dg_color = 'DG-White'
        elif key[0:33] == 'AUC_EM_B466505_L101_G2_Altura_C_M':
            art_work = 'V00794'
            job_setup = 'AUF_CR_VISA_466505_Celeb_DI'
            dg_color = 'DG-White'
            
        elif key[4:22]== 'EM_B466505_L102_G0':
            art_work = 'V00704'
            job_setup = 'AUF_CR_VISA_466505_DI'
            dg_color = 'DG-White'
        elif key[4:22]== 'EM_B466505_L102_G1':
            art_work = 'V00704'
            job_setup = 'AUF_CR_VISA_466505_DI'
            dg_color = 'DG-White'
    
        elif key[4:22]=='EM_B466505_L102_G2':
            art_work = 'V00705'
            job_setup = 'AUF_CR_VISA_466505_DI'
            dg_color = 'DG-White'
            
        elif key[4:19] =='PP_B457036_L401':
            art_work = 'Inf. PP'
            job_setup = 'AUF_CR_PP'
            dg_color = 'Embossing Gold'
        elif key[4:19] =='PP_B465523_L301':
            art_work = 'Sign. PP'
            job_setup = 'AUF_CR_PP'
            dg_color = 'Embossing Gold'
    
    
        else:
            art_work = 'Not Found'
            job_setup = 'Not Found'
            dg_color = 'Not Found'
            
        ptx.add_row([key[8:14], art_work,"", key,value, job_setup, dg_color])
    
    ptx.align = "c"
    ptd=ptx.get_string()
    
    ptx1 = PrettyTable()
    ptx1.field_names = ["Emboss Filename","Supervisor Name","Signature", "  Date  ","  Time  ","   Remark(if any)   "]
    for key, value in names.items():
        
        ptx1.add_row([key,"","","","",""])
    ptx1.align = "c"
    ptd1=ptx1.get_string()
    
    datedmy = str(x)[8:10]+'-'+str(x)[5:7]+'-'+str(x)[0:4]
    with open('AUF_CREDIT_BATCHCARD_'+str(ptime)+'.dat', 'w') as file:
      file.write('                                                '+'BANKING PERSONALISATION BATCH CARD'+'                              '+'Date: '+ptime[0:10]+'\n')
      file.write('                                                       AUC-'+ptime[0:10]+'-'+batch_number+'                                    '+'AUF CREDIT PROJECT(DI)\n\n')
      file.write(str(ptd))
      file.write('\n')
      file.write('TOTAL BATCH QUANTITY:'+str(sum(names.values()))+'\n')
      file.write('                                                   Data upload on Machine\n')
      file.write(str(ptd1))
      file.write('\n\n')
      file.write('PRP: 20.1                                              Rev No: 3.1                                            Date: 20-May-21\n')
      file.write('SEC-3: INTERNAL                                        Owner: Quality Control                                 Status: Issued\n\n')
      file.write('                                                       Page: 1 of 1')
         
    
    
    from fpdf import FPDF
    class PDF(FPDF):
        def header(self):
            self.image('config/colorplast_logo.png', x = 10, y = 5, w = 50, h = 10, type = '', link = '')
            self.ln(8)
    pdf = PDF()
    pdf.add_page('L')
    pdf.set_font("Courier", size=8)
    f = open('AUF_CREDIT_BATCHCARD_'+str(ptime)+'.dat', "r")
    
    for x in f:
        pdf.cell(50, 5, txt = x, ln=True, align = 'L')
        #pdf.image('config/colorplast_logo.png', x = 10, y = 5, w = 50, h = 20, type = '', link = '')
        #pdf.cell(ln=10)
    
    pdf.output('AUF_CREDIT_BATCHCARD_'+ptime[0:10]+'_'+batch_number+'.pdf')
    f.close()
    
    #---------------------------------DELETION LOG-----15.2.2----------------------
    from prettytable import PrettyTable
    ptx = PrettyTable()
    ptx.field_names = (["Client Name", "File Name","File Deletion Date", "Dispatch Date","Data Admin. Name", "Data Admin. Sign.","IT Person Name", "IT Person Sign."])
    
    
    
    
    for key,value in names.items():
        
        ptx.add_row(["AUF Bank", key, "", "", "Data Team", "", "IT Team", ""'\n'])
    ptx.align = "c"
    ptd=ptx.get_string()
    
    with open('AUF_DELETION_LOG_'+datedmy+'.dat', 'w') as file:
      file.write('\n\n                                                                        SEC-IS   |   02.02\n')
      file.write('                                                                        Rev.No.  |   3.0                                                   '+'AUF BANK\n')
      file.write('                                                                        Date :   |   15-Jul-18\n')
      file.write('                                                                 '+'( ***** DATA DELETION LOG ***** )''\n\n\n\n')
      file.write('|  Data Receiving Date - '+datedmy+'  |  '+'  Data Servier - DPP Server/MX Machine  |   '+'  Batch Qty. - '+str(qty)+'   |  '+'  Batch No. - AUF-'+str(x)[8:10]+'-'+str(x)[5:7]+'-'+str(x)[0:4]+'--'+batch_number+'  |  '+'Status -             '+'|''\n\n\n')
      
      file.write(str(ptd))
      file.write('\n\n\n\n')
      #file.write('BATCH NO. OF PM TOOL FOR THIS BATCHCARD :_______________\n')
    from fpdf import FPDF
    class PDF(FPDF):
        def header(self):
            self.image('config/colorplast_logo.png', x = 10, y = 5, w = 50, h = 10, type = '', link = '')
            self.ln(8)
    
    pdf.output('AUF_DELETION_LOG_'+datedmy+'.pdf')
    f.close()
    
    #---------------------------------DELETION LOG ENDS ---------------------------

    print("Batch Generated..........")
    
    print ('\n\n.......Files Processed......Total Credit Card Records: '+str(len(records_list)))
    # for i in range(10,0,-1):
    #     time.sleep(100)
    #     print ('*')
    
    
    
    with open('config/BD_AWB_USING.txt', 'r') as bdfin,open('config/BD_AWB.txt', 'w') as bdfout:
        contents= bdfin.readlines()
        bdfout.writelines(contents)
        bdremainingnew = len(contents)
    bdfin.close()
    bdfout.close()
    with open('config/DL_AWB_USING.txt', 'r') as dtfin,open('config/DL_AWB.txt', 'w') as dtfout:
        contents= dtfin.readlines()
        dtfout.writelines(contents)
        dtremainingnew = len(contents)    
    dtfin.close()
    dtfout.close()
    with open('config/IP_AWB_USING.txt', 'r') as ipfin,open('config/IP_AWB.txt', 'w') as ipfout:
        contents= ipfin.readlines()
        ipfout.writelines(contents)    
        ipremainingnew = len(contents)
    ipfout.close()
    ipfout.close()
        
    with open('AWB_REMAINING_COUNT_NEW.txt','w') as awb_count_new:
        awb_count_new.write('BD   : ' + str(bdremainingnew)+'\n'+'DTDC : '+str(dtremainingnew)+'\nIP   : '+str(ipremainingnew) )
    awb_count_new.close()
    
    
    #os.remove('xxxAUF_Credit_Delhivery_Courier_Connection_Report_.txt')

except Exception as e:    
    traceback.print_exc()

ts = datetime.datetime.now()
ptime = ts.strftime("%d.%m.%Y_%H%M%S")
print(ptime)
 

closeInput = input("Press ENTER to exit")
print ("Closing...")