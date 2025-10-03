
"""
Created on Thu Nov  5 16:22:49 2020

@author: rajeev.jadaun
      AUF_CREDIT_ProcessV.15.5.0.py:16-02-2023[awb allocation for new add-on only ]  
        Rules : 1. Primary + multiple add-on  : Same AWB
        Rules : 2. multiple add-on only cases : Diffrent AWB
        Rules : 3. primary with same account number cases : Diffrent AWB
        TOTAL CARD COUNTS : HOw many cards inserted in single enevelope irresspective with the no of mailers
      AUF_CREDIT_ProcessV.15.4.3.py:14-02-2023[error for dupe check file within 15 days  ]  
      AUF_CREDIT_ProcessV.15.2.4.py:25-08-2022[PP Embo Sorting]
      AUF_CREDIT_ProcessV.15.2.3.py:28-07-2022[Data deletion form]
      AUF_CREDIT_ProcessV.15.2.2.py:23-07-2022[Delhivery Excel generation] 
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
    cwd = os.getcwd()
    primary_card = []
    secondary_card = []
    places = []
    cardnumber_list = []
    bin_list = []

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
    vetta_pp = 0
    zenith_pp = 0
    pp_num =[]
    awb_number = 0
    awb = 0
    # awb_number_bd = []
    # awb_number_dl = []
    # awb_number_ip = []
    pct_id_val = []
    routing_code = ''
    courier = ''
    row = []
    account_number_list = []
    pri_account_number = []
    add_on_account_number = []
    pp_list = []
    records_list = []
    s_no = 0
    
    total_primary_count = 0
    total_pp_count = 0
    count = 0
    file_count_num =0
    
    
    ts = datetime.datetime.now()
    ptime = ts.strftime("%d.%m.%Y_%H%M%S")
    ptime_1 = ts.strftime("%d.%m.%Y")
    print(ptime)
    print(ptime)
    file_check = glob.glob('L2CDZU*')
    if len(file_check)==0:
        print("No Input Files present")
    else:
        
        
        #---------------------BATCH SERIES--------------------------------------------------------------    
        try:
            with open('config/AUC_batch_series', 'r') as fin:
                batch_series_data = fin.readlines()
                batch_number = batch_series_data[0].rstrip()
            fin.close()
        except:
            print("Batch Series Finished!!!!")
            
            
            
            
            
    
    #---------------------------FEES --------------------------------------------------------   
        with open('config/Fees_console.csv','r') as data_file_pct:
            contents = data_file_pct.readlines()
            for line in contents:
                line = line.split(',')
                # print(line[1])
                pct_id_val.append(line[1])
        data_file_pct.close()
    
        
        #  #----------------AWB SERIES DUP FILES-------------------------------------------------------------------
        # with open('config/BD_AWB.txt', 'r') as bdfin, open('config/BD_AWB_USING.txt', 'w') as bdfout:
        #     contents = bdfin.readlines()
        #     bdfout.writelines(contents)
        # bdfin.close()
        # bdfout.close()
        # with open('config/DL_AWB.txt', 'r') as dtfin, open('config/DL_AWB_USING.txt', 'w') as dtfout:
        #     contents = dtfin.readlines()
        #     dtfout.writelines(contents)
        # dtfin.close()
        # dtfout.close()
        # with open('config/IP_AWB.txt', 'r') as ipfin, open('config/IP_AWB_USING.txt', 'w') as ipfout:
        #     contents = ipfin.readlines()
        #     ipfout.writelines(contents)
        # ipfin.close()
        # ipfout.close()
        
        
        
        
        # sorting defination for EMBOSSA file #-----------------------------------------------------------------------------------
        def my_sort_emb(line):
            line_fields = line.strip().split()
            couriersort = line_fields[-1]
            return couriersort
        
        def pp_sort_emb(line):
            line_fields = line.strip().split()
            couriersort = line_fields[-1]
            couriersort = couriersort[-1]
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
            return couriersort
      
        
      #-----------------------PP DUP CHECK------------------------------------------------------------   
        def pp_dup_check(number):
            with open('./config/AUF_CREDIT_PP_CONSOLE.txt','r') as file_read:
                contents = file_read.readlines()
                new_contents = [x[:-1] for x in contents]
                if number in new_contents:
                    print("PP duplicate number found : "+number)
                elif number in pp_num:
                    print("PP duplicate number found : "+number)
                
                else:
                    #    ("not found")
                    pp_num.append(number)
                    
            file_read.close()
            return number
                
#=============================================Fees-Logic=============================================                
        def fees(logo,pct):   
            joining_fees = ""
            annual_fees = ""
            with open("./config/Fees_console.csv","r") as data_read:
                contents = data_read.readlines()
                #print(str(logo)+"-"+str(pct))
                
                for line in contents:
                    line = line.split(",")
                    logo_id = line[0]
                    pct_id = line[1]
                    if (logo_id == logo) and (pct_id == pct):
                        joining_fees = line[2]
                        annual_fees = line[3].rstrip()
                        break
                    
                return(joining_fees,annual_fees)
    
        def program_closed():#=============================================del extra files
            closeInput = input("Press ENTER to exit")
            print ("Closing...")  
            del_file = glob.glob("*.txt")
            for dem in del_file:
                try:
                    os.remove(dem)
                except:
                    print(dem+"  file cannot be deleted")
            
            del_file = glob.glob("*.csv")
            del_file.remove(f"AUF_File_DupeCheck_{ptime_1}.csv")
            for dem in del_file:
                try:
                    os.remove(dem)
                except:
                    print(dem+"  file cannot be deleted")
            
            del_file = glob.glob("*.dat")
            for dem in del_file:
                try:
                    os.remove(dem)
                except:
                    
                    print(dem+"  file cannot be deleted")
            raise SystemExit
            
                 
    
    
    
    
 
        
        def courier_assign(pincode_1):#=============================================courier_assign
            with open('config/PINCODE_MASTER.csv', 'r') as pin:
                routing_codewe = pin.readlines()
                flag = 0
                courier_1 = ''
                routing_code_1 = ''
                # customer_code = ''
                for line in routing_codewe:
                    pincodedata = line.split(',')
                    if pincode_1 != '':
                        # and pincodedata[4]=='BLUEDART':
                        if pincode_1 in pincodedata[0]:
                            flag = 1
    
                            courier_1 = pincodedata[2].rstrip()
                            routing_code_1 = pincodedata[1].rstrip()
                            break
                if flag == 0:
                    courier_1 = 'Indiapost'
                    routing_code_1 = 'BNPL-921-413'
                    # courier_1 = str(courier_1)
            pin.close()
            return(courier_1,routing_code_1)
        
        def jdtodatestd(jdate):#=============================================courier_assigndate converson
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
        
        def ip_weight(cardaction):#=============================================ip weight assign
            weight_ip = ''
            try:   
                with open('config/AU_Credit_Variant_Weight_Table.csv', 'r') as ip_we:
                    contents = ip_we.readlines()
                    for line in contents:
                        content = line.split(',')
                        try:
                            if (cardaction == content[0]):
                                weight_ip = content[1].rstrip()
                            
                        except:
                            weight_ip = ''
            except:
                print('Error in AU_Credit_Variant_Weight_Table.csv against card_action : '+cardaction)
                
            
            return weight_ip
                            
        def awb_assign(courier_2):#=============================================awb_assign
            global bd_num,dl_num,ip_num,awb
            if courier_2 == 'Bluedart':
                try:
                    with open('config/BD_AWB.txt', 'r') as bdfin:
                        bdawb1 = bdfin.readlines()
                        awb_check = (len(bdawb1)-(bd_num + 1))
                        # if awb_check!=0:
                        awb = bdawb1[bd_num].rstrip()
                        bd_num += 1    
                except:
                    print("BD Awb Finished, Remaining Count : "+str(len(bdawb1)))
                    program_closed()
                         
                        
                    
            elif courier_2 == 'Delhivery':
                try:
                    with open('config/DL_AWB.txt', 'r') as dlfin:
                        dlawb = dlfin.readlines()
                        awb_check = (len(dlawb)-(dl_num + 1))
                        # if awb_check!=0:
                        awb = dlawb[dl_num].rstrip()
                        dl_num += 1
                            
                except:
                    print("DTDC Awb Finished, Remaining Count : "+str(len(dlawb)))
                    program_closed()
                         
                   
            elif courier_2 == 'Indiapost':
                try:
                    
                    with open('config/IP_AWB.txt', 'r') as ipfin:
                        ipawb = ipfin.readlines()
                        awb_check = (len(ipawb)-(ip_num + 1))
                        # if awb_check!=0:
                        awb = ipawb[ip_num].rstrip()
                        ip_num += 1
                except:
                    print("IP Awb Finished , Remaining Count : "+str(len(ipawb)))
                    program_closed()
                   
            return(awb)    
        
#=============================================File-Prcocessing starts=============================================   
   
   
   
        file_name = glob.glob('L2CDZU*')
        
        if len(file_name)==0:
            print("No Input Files present")
        else:
            #=============================================File Dupe Check
            with open("config/File_DupeCheck.csv",'r') as dupecheck_file,open(f"AUF_File_DupeCheck_{ptime_1}.csv",'a') as dupecheck_file_cust:
                
                
                dupecheck_file_filecontents = dupecheck_file.readlines()
                Types = [line.split(":") for line in dupecheck_file_filecontents]
                filenames_list = [Type[1].rstrip() for Type in Types]
                # print(filenames_list)
                # print(file_name)
                ts = time.time()
                x = (ts)
                #filenames = glob.glob('L2CDZU*')
                merge_output_file = 'del_output_file_'+str(x)+'_.txt'
                 
                for i in range(len(file_name)):
                    # print(file_name[file_count_num])
                    if file_name[file_count_num] in filenames_list:
                        pos_1 = filenames_list.index(file_name[file_count_num])
                        date_1_old_file = dupecheck_file_filecontents[pos_1][0:5]
                        # print(date_1_old_file)
                        date_1_old_file = "20" + date_1_old_file
                        # print(date_1_old_file)
                        # datestd = datetime.datetime.strptime(str(date_1_old_file), '%Y%j').date()
                        # print(datestd)
                        dupecheck_file_cust.write("Duplicate files found : "+str(file_name[file_count_num])+" old file date : "+jdtodatestd(date_1_old_file)+"\n")
                        
                        del file_name[file_count_num]
                        file_count_num-=1
                    else:
                        with open((file_name[file_count_num]), 'r') as filehandle:
                            filecontents = filehandle.readlines()
                            del filecontents[0]
                            del filecontents[-1]
                            
                            with open(merge_output_file, 'a') as outfile:
                                for fname in filecontents:
                                    outfile.write(fname)
                        filehandle.close()
                     
                    file_count_num+=1
           #=============================================  
          
            if len(file_name)==0:
                print("\n\nAll Input Files are duplciate within 15 days!!!")
                program_closed()
            
            #==========================================================================================
            merge_filename = glob.glob('del_output_file*.txt')
            with open('merge_output_file_'+str(x)+'.txt', 'w') as outfile:
                for fname in merge_filename:
                    with open(fname) as infile:
                        for line in infile:
                            outfile.write(line)
                            records_list.append(line)
            
                            # for i in enumerate(line):
                            account_number = line[38:54]
                            card_holder_type = line[2089:2090]
                            
                            if  account_number not in pri_account_number and  card_holder_type == "1":
                                pri_account_number.append(account_number)
                            elif  card_holder_type == "0":
                                add_on_account_number.append(account_number)
                            file_credit_card_em = line[:]
                                
            
                            #with open('AUC_EM_account_'+str(account_number)+'_'+str(ptime)+'.txt', 'a') as em_file:
                            with open('AUC_EM_account.txt', 'a') as em_file:
                                em_file.write(file_credit_card_em)
                                
                                    
                            em_file.close()
            outfile.close()
            
            for acc in add_on_account_number:
                if acc not in pri_account_number:
                    for i in range(int(add_on_account_number.count(acc))-1):
                        add_on_account_number.remove(acc)
            
            pri_account_number+=add_on_account_number #for toal no of cards as per 
                    
            #==========================================================================================
            auf_pp_output_header = 'Account_Number,Logo,Card_Number,Card_Holder_name,Card_action,Priority_Pass_Number,PP_issuance_date'
            
            with open('Priority_Pass_Data_'+str(ptime[0:10])+'.csv', 'w') as pp_file_auf_h:
                pp_file_auf_h.write(auf_pp_output_header + '\n')
                
                #print (file_pp_merge)
            pp_file_auf_h.close()
            
                  
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
            
                            # for i in enumerate(line_acc):
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
                            
                            # mailer_name_acc = mailer_name1_acc+' '+mailer_name2_acc+' '+mailer_name3_acc
                            mailer_name_acc = mailer_name1_acc
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
                            pp_count=''
                            totol_card_count = pri_account_number.count(account_number_acc)
                            courier = courier_assign(mailer_postal_code_acc)[0]
                            courier = courier.title()
                            routing_code = courier_assign(mailer_postal_code_acc)[1]
                            
    # =============================================================================
    #                         if card_holder_type_acc == '1' or (card_holder_type_acc == '0' and account_number_acc not in account_number_list):
    #                             # row=[]
    #                             #card_type = 'Primary Card'
    #                             # account_number_list.append(account_number_acc)
    #                             
    #                             awb_number = awb_assign(courier)
    #                             
    #         
    #                         elif card_holder_type_acc == '0' and account_number_acc in account_number_list:
    #                             #index=np.where(arr == 15)
    #                             pos = account_number_list.index(account_number_acc)
    #                             awb_number = account_number_list[pos+1]
    #                             #add_on_mask_pan = mask_pan_acc
    #                         else:
    #                             awb_number = ''
    #                             #add_on_mask_pan = ''
    #                         # if card_holder_type_acc == '1':
    #                         
    #                         if card_holder_type_acc == '1':
    #                             account_number_list.extend([account_number_acc, awb_number])
    # =============================================================================
                            try: 
                                if totol_card_count == 1 :
                                    awb_number = awb_assign(courier)
                                
                                elif account_number_acc not in account_number_list:
                                        #index=np.where(arr == 15)
                                        awb_number = awb_assign(courier)
                                        account_number_list.extend([account_number_acc, awb_number])
                                
                                elif account_number_acc in account_number_list:        
                                        pos = account_number_list.index(account_number_acc)
                                        awb_number = account_number_list[pos+1]
                                        #add_on_mask_pan = mask_pan_acc
                                else:
                                    awb_number = ''
                            except Exception as e:
                                print("Error while assigning awb number : error msg : "+ e)
                            
                           
                            
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
                                product = 'Altura'
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
                                    product = 'AlturaPlusBlue'
                                elif gender_code_acc == '1':
                                    varient = 'AlturaPlusBlue'
                                    product = 'AlturaPlusBlue'
                                elif gender_code_acc == '2':
                                    varient = 'AlturaPlusRuby'
                                    product = 'AlturaPlusRuby'
                            
                            elif c_bin_acc == '465523'  and  logo_acc == '301': 
                                varient = 'Vetta'
                                product = 'Vetta'
                            
                            elif c_bin_acc == '457036'  and  logo_acc == '401': 
                                #ADDED on 26052022 as per customer requiement new varient
                                #young indians with pastic id 
                                if plastic_id == '          ':
                                    varient = 'Zenith'
                                    product = 'Zenith'
                                elif plastic_id == '0000000001':
                                    varient = 'Zenith_CII_Young_Indian'
                                    product = 'Zenith_CII_Young_Indian'
                                
                                
                            #New BIN ADDITON-21-04-2022
                            elif c_bin_acc == '406977'  and  logo_acc == '501':
                                varient = 'AU_BANK_LIT_CREDIT_CARD'
                                product = 'AU_BANK_LIT_CREDIT_CARD'
                            
                            elif c_bin_acc == '483976'  and  logo_acc == '601':
                                varient = 'Corporate_Reward_Credit Card'
                                product = 'Corporate_Reward_Credit Card'
                            elif c_bin_acc == '483976'  and  logo_acc == '602':
                                varient = 'Corporate_Credit_Card'
                                product = 'Corporate_Credit_Card'
                            elif c_bin_acc == '483976'  and  logo_acc == '603':
                                varient = 'Secured_Corporate_Credit_Card'
                                product = 'Secured_Corporate_Credit_Card'
                            
                            elif c_bin_acc == '483974'  and  logo_acc == '701':
                                varient = 'Purchase Reward Credit Card'
                                product = 'Purchase Reward Credit Card'
                            elif c_bin_acc == '483974'  and  logo_acc == '702':
                                varient = 'Purchase Credit Card'
                                product = 'Purchase Credit Card'
                            elif c_bin_acc == '483974'  and  logo_acc == '703':
                                varient = 'Secured_Purchase_Credit_Card'
                                product = 'Secured_Purchase_Credit_Card'
                            
                            elif c_bin_acc == '483894'  and  logo_acc == '801':
                                varient = 'Business_Reward_Credit_Card'
                                product = 'Business_Reward_Credit_Card'
                            elif c_bin_acc == '483894'  and  logo_acc == '802':
                                varient = 'Secured Business Credit Card'
                                product = 'Secured Business Credit Card'
                            elif c_bin_acc == '483894'  and  logo_acc == '803':
                                varient = 'Business Cashback Credit Card'
                                product = 'Business Cashback Credit Card'
        
                            
        
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
                            
        
                            ip_weigh = ip_weight(varient)
                            if ip_weigh == '':
                                ip_weigh = ip_weight(card_action)
                                
                            #print(card_holder_name_acc)
                            joining_fees = fees(logo_acc,pct_id)[0]
                            annual_fees = fees(logo_acc,pct_id)[1]
                            
                            if card_holder_type_acc=='0':
                                totol_addon_card_count = '1'
                            else:
                                totol_addon_card_count = '0'
                            totol_card_count = str(totol_card_count)
                            
                            
                            file_credit_card_ff_acc = ' '+'|'+c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+ref_number+'|'+card_type+'|'+mask_pan_acc+'|'+account_number_acc+'|'+card_action+'|'+salutation_acc+'|'+mailer_name_acc+'|'+mailer_address1_acc+'|'+mailer_address2_acc+'|' + mailer_address3_acc+'|'+mailer_address4_acc+'|'+mailer_city_acc+'|'+mailer_state_code_acc+'|'+mailer_postal_code_acc+'|'+mailer_mob_acc+'|' + customer_id_acc+'|'+cr_card_limit+'|'+billing_cycle+'|'+superscript+'|' + print_card_holder_name_acc+'|' +  pct_id+'|'  # +jdtodatestd(date_acc)
                            file_credit_card_ff_acc_allocation = ' '+'|'+account_number_acc + '|'+mask_pan_acc+'|'+mailer_name_acc+'|'+'|'+'|'+'|'+'|'
                            file_credit_card_ff_acc_primary = ' '+'|'+account_number_acc + '|'+mask_pan_acc+'|'+mailer_name_acc+'|'+'|'+'|'+'|'+'|'
                            file_credit_card_ff_acc_addon = ' '+'|'+account_number_acc + '|'+'|'+mailer_name_acc+'|'+mask_pan_acc+'|'+'|'+'|'+'|'
                            file_credit_card_ff_acc_3_primary = card_action+'|'+'1|'+totol_addon_card_count+'|'+totol_card_count+'|'+c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+mailer_address1_acc+'|'+mailer_address2_acc+'|'+mailer_address3_acc+'|'+mailer_address4_acc+'|'+mailer_city_acc + '|'+mailer_state_code_acc+'|'+mailer_postal_code_acc+'|'+mailer_mob_acc+'|'+customer_id_acc+'|'+cr_card_limit+'|' + billing_cycle+'|'+superscript+'|'+print_card_holder_name_acc + '|'+joining_fees+'|'+annual_fees + '|'+str(jdtodatestd(date_acc))
                            file_credit_card_ff_acc_3_primary_replace = card_action+'|'+'1|'+totol_addon_card_count+'|'+totol_card_count+'|'+c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+mailer_address1_acc+'|'+mailer_address2_acc+'|'+mailer_address3_acc+'|'+mailer_address4_acc+'|'+mailer_city_acc + '|'+mailer_state_code_acc+'|'+mailer_postal_code_acc+'|'+mailer_mob_acc+'|'+customer_id_acc+'|'+cr_card_limit+'|' + billing_cycle+'|'+superscript+'|'+print_card_holder_name_acc
                            file_credit_card_ff_acc_3_addon = card_action+'|'+'0|'+totol_addon_card_count+'|'+totol_card_count+'|'+c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+mailer_address1_acc+'|'+mailer_address2_acc+'|'+mailer_address3_acc+'|'+mailer_address4_acc+'|'+mailer_city_acc +'|'+mailer_state_code_acc+'|'+mailer_postal_code_acc+'|'+mailer_mob_acc+'|'+customer_id_acc+'|'+cr_card_limit+'|' +billing_cycle+'|'+superscript+'|'+print_card_holder_name_acc +'|'+joining_fees+'|'+annual_fees +'|'+str(jdtodatestd(date_acc))
                            file_credit_card_ff_acc_3_addon_replace = card_action+'|'+'0|'+totol_addon_card_count+'|'+totol_card_count+'|'+c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+mailer_address1_acc+'|'+mailer_address2_acc+'|'+mailer_address3_acc+'|'+mailer_address4_acc+'|'+mailer_city_acc +'|'+mailer_state_code_acc+'|'+mailer_postal_code_acc+'|'+mailer_mob_acc+'|'+customer_id_acc+'|'+cr_card_limit+'|' +billing_cycle+'|'+superscript+'|'+print_card_holder_name_acc 
                            indianpost_courier_1 = '||'+ref_number+'|'+mailer_city_acc+'|'+mailer_postal_code_acc+'|'+mailer_name_acc+'|' + mailer_address1_acc+'|'+mailer_address2_acc+'|'+mailer_address3_acc + '|'+mailer_address4_acc+'|'+mailer_mob_acc+'||'
                            file_credit_card_ff_acc_new = ' '+'|'+account_number_acc+'|'+ref_number+'|'+mask_pan_acc+'|'+salutation_acc+' '+mailer_name_acc + '|'+pp_cardnumber_acc+'|'+print_exp_date_acc+'|'+varient + '|'+logo_acc+'|' + gender_code_acc  # +jdtodatestd(date_acc)
                            file_credit_card_em_acc = line_acc[:].rstrip('\n')
                            pct_id_data = str(ptime[0:10])+','+account_number_acc+','+logo_acc+','+pct_id+','+mask_pan_acc+','+card_holder_name_acc.rstrip()+','+card_action
                            #header='Sr. No|Account Number|Primary Card number|Customer Name|Add-on Card 1|Add-on Card 2|Add-on Card 3|Add-on Card 4|PP  Card No_Primary|PP  Card No_Addon1|PP  Card No_Addon2|PP  Card No_Addon3|Ref no.|AWB. No.|Courier|Courier Code|Card Action|Primary Count|Add-on Count|Total Cards|Bin|Logo|Gender Code|Varient|Address Line 1|Address Line 2|Address Line 3|Address Line 4|City|State Code|Postal Code|Mobile Number|Cust Unique ID|Credit Limit|Statement Date |Extention|Embo_Name|Joining Fees|Annual Fees|Card Issuance Date'
                            bin_list.append(c_bin_acc+logo_acc+gender_code_acc)
                            bin_list = list(dict.fromkeys(bin_list))
                            qty = ''    
            
                             
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
                                        # pp_cardnumber_acc = pp_cardnumber_acc+'01'
                                        primary_card.append(cardnumber_acc)
                    
                                    if card_holder_type_acc == '0':
                                        secondary_card.append(cardnumber_acc)
                    
                            
                            if ((c_bin_acc == '465523' and card_holder_type_acc=='1') or c_bin_acc == '457036'):
                                if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                                    if c_bin_acc == '465523' :#Vetta cards
                                        with open('config/VETTA_PP_NUMBER.csv', 'r') as vetta_pp_in:
                                            try:
                                                vetta_pp_total    = vetta_pp_in.readlines()
                                                pp_cardnumber_acc = vetta_pp_total[vetta_pp].rstrip()
                                                vetta_pp+=1
                                            except:
                                                print("VETTA PP NUMBER Finished!!!! Remaining Count : "+str(len(vetta_pp_total)))
                                                program_closed()
                                            
                                    
                                        
                                    elif c_bin_acc == '457036' :#Zenith cards
                                        try:
                                            with open('config/ZENITH_PP_NUMBER.csv', 'r') as zenith_pp_in:
                                                zenith_pp_total   = zenith_pp_in.readlines()
                                                pp_cardnumber_acc = zenith_pp_total[zenith_pp].rstrip()
                                                zenith_pp+=1
                                        except:
                                            print("ZENITH PP NUMBER Finished!!!!   Remaining Count : "+str(len(zenith_pp_total)))
                                            program_closed()
                                        
                                    
                                    pp_cardnumber_acc = pp_dup_check(pp_cardnumber_acc)
                                    
                                    pp_count = '1'
                            
                           
                            track1_acc = '%PP/'+salutation_acc+'/'+print_card_holder_name_acc+'//''?'
                           
                            track2_acc = ';'+pp_cardnumber_acc+'=' +(pp_exp_date_acc[0:2]+'20'+str(int(pp_exp_date_acc[2:4])+3)) + '?'
                            
                            file_credit_card_ff_acc_2_primary = pp_cardnumber_acc+'|'+'|'+'|' +'|'+ref_number+'|'+str(awb_number) +'|'+courier+'|'+routing_code+'|'
                            
                            file_credit_card_ff_acc_2_addon = pp_cardnumber_acc+'|'+'|'+'|' '|'+ref_number+'|'+str(awb_number) + '|'+courier+'|'+routing_code+'|'
            
                            auf_pp_output = account_number_acc+','+logo_acc+','+mask_pan_acc+',' +card_holder_name_acc.rstrip()+','+card_action+',' +pp_cardnumber_acc+','+str(ptime[0:10])
                            
                            auf_pp_output_bank = pp_cardnumber_acc+','+str(ptime[0:10])+','+(pp_exp_date_acc[0:2]+'20'+str(int(pp_exp_date_acc[2:4])+3))+','+account_number_acc+','+card_holder_name_acc.rstrip()
                            
                            bluedart_courier = ref_number+'|'+mailer_name_acc+'|'+mailer_address1_acc+'|'+mailer_address2_acc+'|'+mailer_address3_acc+'-' + mailer_address4_acc+'|'+mailer_city_acc+'|'+mailer_state_code_acc +'||'+mailer_postal_code_acc+'|' +mailer_mob_acc+'|'+str(awb_number)
                            
                            delhivery_courier = str(awb_number)+'|'+ref_number+'|'+mailer_name_acc+'|'+mailer_city_acc+'|'+mailer_state_code_acc+'||'+mailer_address1_acc+' '+mailer_address2_acc+' '+mailer_address3_acc+' '+mailer_address4_acc+'|'+mailer_postal_code_acc+'|'+mailer_mob_acc+'|' + '250|Prepaid|500|Secure Deliverables|AU Centre, 3rd Floor (Credit Card Division), Sunny Trade Centre, New Atish Market, Jaipur, Rajasthan 302019|302019|AU Small Finance Bank Ltd|AU Small Finance Bank Limited AU Centre, 3rd, 5th, 6th & 7th Floor, Sunny Trade Centre, New Atish Market, Jaipur, Rajasthan  302019|True|True'
                            
                            indianpost_courier = '||'+ref_number+'|'+mailer_city_acc+'|'+mailer_postal_code_acc+'|'+mailer_name_acc+'|'+mailer_address1_acc +'|'+mailer_address2_acc+'|'+mailer_address3_acc+'|' +mailer_address4_acc+'|'+mailer_mob_acc+'||'+str(awb_number)  +'|'+str(ip_weigh)
                            
                            allocation_data_primary = '|'+account_number_acc+'|'+mask_pan_acc+'|'+print_card_holder_name_acc+'|||||'+pp_cardnumber_acc+'||||'+ref_number+'|' +str(awb_number)+'|'+courier+'|'+routing_code+'|'+card_action+'|1|'+totol_addon_card_count+'|'+totol_card_count+'|'+c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+mailer_address1_acc+'|'+mailer_address2_acc+'|'+mailer_address3_acc+'|' +mailer_address4_acc+'|'+mailer_city_acc+'|'+mailer_state_code_acc+'|'+mailer_postal_code_acc+'|' +mailer_mob_acc+'|'+customer_id_acc+'|'+pp_count+'|'+joining_fees +'|'+annual_fees+'|'+str(jdtodatestd(date_acc))                
                            
                            allocation_data_addon = '|'+account_number_acc+'||'+card_holder_name_acc.rstrip()+'|'+mask_pan_acc+'|||||'+pp_cardnumber_acc+'|||'+ref_number+'|'+str(awb_number)+'|'+courier+'|'+routing_code+'|'+card_action+'-Additional Card'+'|0|'+totol_addon_card_count+'|'+totol_card_count+'|'+c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+mailer_address1_acc +'|'+mailer_address2_acc+'|'+mailer_address3_acc+'|'+mailer_address4_acc+'|'+mailer_city_acc+'|'+mailer_state_code_acc+'|' +mailer_postal_code_acc+'|'+mailer_mob_acc+'|'+customer_id_acc+'|' +pp_count+'|'+joining_fees+'|'+annual_fees +    '|'+str(jdtodatestd(date_acc))
                            
                            if ((c_bin_acc == '465523' and card_holder_type_acc=='1') or c_bin_acc == '457036'):
                                if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                                    if mask_pan_acc not in filecontents:
                                        file_pp = '#0#'+mask_pan_acc+'#1#'+pp_cardnumber_acc+'#2#'+track1_acc+'#3#'+track2_acc +'#4#'+ (pp_exp_date_acc[0:2]+'/'+str(int(pp_exp_date_acc[2:4])+3)) +'#5#'+salutation_acc +' '+print_card_holder_name_acc+'#6#'
                                        
                                        file_pp_merge = account_number_acc+'|'+ref_number+'|'+mask_pan_acc+'|'+salutation_acc+' ' +print_card_holder_name_acc+'|'+pp_cardnumber_acc+'|' + (pp_exp_date_acc[0:2]+'/'+str(int(pp_exp_date_acc[2:4])+3)) +'|'+varient+'|'+logo_acc+'|'+gender_code_acc
            
                            if courier == 'Indiapost':
                                with open('xxxAUF_Credit_IndiaPost_Courier_Connection_Report_.txt', 'a') as ff_ip_acc:
                                    # ff_ip_acc.write(indianpost_courier_1+indianpost_courier_2+'\n')
                                    ff_ip_acc.write(indianpost_courier+'\n')
                                ff_ip_acc.close()
                            elif courier == 'Delhivery':
                                with open('xxxAUF_Credit_Delhivery_Courier_Connection_Report_.txt', 'a') as ff_dl_acc:
                                    ff_dl_acc.write(delhivery_courier+'\n')
                                ff_dl_acc.close()
                            elif courier == 'Bluedart':
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
                                        
# =============================================================================
#                                         with open('config/Priority_Pass_Data_AUF_BANK.csv', 'a') as pp_file_auf_ha:
#                                             pp_file_auf_ha.write(auf_pp_output_bank+'\n')
#                                         pp_file_auf_ha.close()
# =============================================================================
                                        pp_list.append(auf_pp_output_bank)
                            
                            if (c_bin_acc == '483974' ):
                                with open('ALERT!!___NEW BIN 483974 RECEIVED.dat', 'a') as alert_ff:
                                    alert_ff.write(c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+ref_number+'|'+card_type+'|'+mask_pan_acc+'|'+account_number_acc+'|'+card_action+'\n')
                                alert_ff.close()
                            
                            
                            #Alert for new bin -483974
                            if (c_bin_acc == '483974' ):
                                with open('ALERT!!___NEW BIN 483974 RECEIVED.dat', 'a') as alert_ff:
                                    alert_ff.write(c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+ref_number+'|'+card_type+'|'+mask_pan_acc+'|'+account_number_acc+'|'+card_action+'\n')
                                alert_ff.close()
                            
                            if pct_id not in pct_id_val:
                                with open('Wrong pct_id data_'+str(ptime)+'.txt','a') as data_file:
                                    if count == 0:
                                        data_file.write('Date,Account_Number,Logo_acc,Pct_id,Mask_pan_acc,Card_holder_name,card_action\n')
                                        count+=1
                                    data_file.write(pct_id_data + '\n')
                                    
                                data_file.close()
                                        
                                        
                
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
                    df.to_excel(name_ff[2:-4]+'_'+ptime[0:10]+'--'+ str(s_no)+'.xlsx', 'Sheet1', index=False)
                    
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
                    df.to_excel(name_ff[2:-4]+'_'+ptime[0:10]+ '--'+str(s_no) +'.xlsx', 'Sheet1', index=False) 
                    
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
                    df.to_excel(pp_name_ff[2:-4]+'_'+ptime[0:10]+ '--'+str(s_no) +'.xlsx', 'Sheet1', index=False) 
                    
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
                    foutfile.write('SNO|Barcode_Value|REFERANCE NUMBER|CITY|PINCODE|NAME|ADDRESS 1|ADDRESS 2|ADDRESS 3|ADDRESSEE EMAIL|ADDRESSEE MOBILE|SENDER MOBILE|POD REQUIRED|Weight'+'\n')
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
                df.to_excel('AUF_Credit_IndiaPost_Courier_Connection_Report_'+str(ptime[0:10])+'--' +str(s_no)+'.xlsx', 'Sheet1', index=False)
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
                df.to_excel('AUF_Credit_Delhivery_Courier_Connection_Report_'+str(ptime[0:10])+'--'+str(s_no)+'.xlsx', 'Sheet1',index=False)
                os.remove('xxxAUF_Credit_Delhivery_Courier_Connection_Report_.txt')
                os.remove('AUF_Credit_Delhivery_Courier_Connection_Report_.txt')
            
            Bluedart_Courier = 'xxxAUF_Credit_Bluedart_Courier_Connection_Report_.txt'
            if Path(Bluedart_Courier).is_file():
                records_list = []
                s_no = 0
                with open('xxxAUF_Credit_Bluedart_Courier_Connection_Report_.txt', "r") as ff, open('AUF_Credit_Bluedart_Courier_Connection_Report_.txt', "w") as foutfile:
                    foutfile.write(
                        'Refrence Number|Customer Name|ADDRESS1|ADDRESS2|ADDRESS3|CITY|STATE|COUNTRY|PINCODE|CONTACT1|AWB'+'\n')
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
                df.to_excel('AUF_Credit_Bluedart_Courier_Connection_Report_' +str(ptime[0:10])+'--'+str(s_no)+'.xlsx', 'Sheet1', index=False)
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
            # df = pd.read_csv('AUF_FF_MIS_MERGE_'+str(ptime)+'.txt',encoding= 'unicode_escape', sep='|', dtype=object)
            # df.to_excel('AUF_FF_MIS_MERGE_'+str(ptime)+'-' +str(s_no)+'.xlsx', 'Sheet1', index=False)
            os.remove('xxAUF_FF_MIS_MERGE_'+str(ptime)+'.txt')
            # os.remove('AUF_FF_MIS_MERGE_'+str(ptime)+'.txt')
            
            
            with open('xxAUF_Credit_Data_Allocation_Report_.txt', "r") as ff, open('AUF_Credit_Data_Allocation_Report_.txt', "w") as foutfile:
                records_list = []
                s_no = 0
                foutfile.write('Sr. No|Account Number|Primary Card number|Customer Name|Add-on Card 1|Add-on Card 2|Add-on Card 3|Add-on Card 4|PP  Card No_Primary|PP  Card No_Addon1|PP  Card No_Addon2|PP  Card No_Addon3|Ref no.|AWB. No.|Courier|Courier Code|Card Action|Primary Count|Add-on Count|Total Cards|Bin|Logo|Gender Code|Varient|Address Line 1|Address Line 2|Address Line 3|Address Line 4|City|State Code|Postal Code|Mobile Number|Cust Unique ID|Total PP Count|Joining Fees|Annual/Monthly Fees|Card Issuance Date'+'\n')
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
            df.to_excel('AUF_Credit_Data_Allocation_Report_'+str(ptime[0:10]) +'--'+str(s_no) +'+'+str(total_pp_count)+'.xlsx', 'Sheet1', index=False)
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
            qty1 = sum(names.values())
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
            #---------------------------------BatchCard ENDS ---------------------------
            
            #---------------------------------DELETION LOG-----15.2.2----------------------
            from prettytable import PrettyTable
            ptx = PrettyTable()
            ptx.field_names = (["Client Name", "File Name","File Deletion Date", "Dispatch Date","Data Admin. Name", "Data Admin. Sign.","IT Person Name", "IT Person Sign."])
            
            for key,value in names.items():
                
                ptx.add_row(["AUF Bank", key, "", "", "Data Team", "", "IT Team", ""])
            ptx.align = "l"
            ptd=ptx.get_string()
            # print(ptd)
            with open('AUF_DELETION_LOG_'+datedmy+'.dat', 'w') as file:
              file.write('\n\n                                                                        SEC-IS   |   02.02\n')
              file.write('                                                                        Rev.No.  |   3.0                                                   '+'AUF CREDIT PROJECT(DI)\n')
              file.write('                                                                        Date :   |   15-Jul-18\n')
              file.write('                                                                 '+'( ***** DATA DELETION LOG ***** )''\n\n')
              file.write('|  Data Receiving Date - '+ptime[0:10]+'  |  '+'  Data Server - DPP Server/MX Machine  |   '+'  Batch Qty. - '+str(sum(names.values()))+'   |  '+'  Batch No. - AUC-'+ptime[0:10]+'-'+batch_number+'    |  '+'  Status -                  '+'|''\n')
              
              file.write(str(ptd).rstrip())
              file.write('\n')
              #file.write('BATCH NO. OF PM TOOL FOR THIS BATCHCARD :_______________\n')
            # from fpdf import FPDF
            class PDF1(FPDF):
                def header(self):
                    self.image('config/colorplast_logo.png', x = 10, y = 5, w = 50, h = 10, type = '', link = '')
                    self.ln(8)
            
            pdf1 = PDF1()
            pdf1.add_page('L')
            pdf1.set_font("Courier", size=6.5)
            f = open('AUF_DELETION_LOG_'+datedmy+'.dat', "r")
            
            for x in f:
                pdf1.cell(50, 5, txt = x, ln=True, align = 'L')
                #pdf.image('config/colorplast_logo.png', x = 10, y = 5, w = 50, h = 20, type = '', link = '')
                #pdf.cell(ln=10)
            
            
            pdf1.output('AUF_DELETION_LOG_'+ptime[0:10]+'.pdf')
            f.close()
            
            #---------------------------------DELETION LOG ENDS ---------------------------
        
            print("Batch Generated..........")
            
            
            path = ('.')
            ext = "txtt"
            
            for f in os.listdir(path):
                fpath = os.path.join(path, f)
            
                if os.path.isfile(fpath) and fpath.endswith(ext):
                    time = datetime.datetime.fromtimestamp(os.path.getctime(fpath)).strftime("%d-%m-%Y---"+str(s_no) +'+'+str(total_pp_count))
                    name='AUC_'+time
                    os.makedirs(os.path.join(path, name), exist_ok=True)
                    os.makedirs(os.path.join("A:/Sdrive/LIVE/AU_Credit/", name), exist_ok=True)
                    os.replace(fpath, os.path.join(path, name, f))
            
            
            
               
            from distutils.dir_util import copy_tree        
            
            fromDirectory =  os.getcwd()
            aaa = fromDirectory+'/'+name
            
            toDirectory = "A:/Sdrive/LIVE/AU_Credit/"
            bbb = toDirectory +name
            # print(aaa)
            # print(bbb)
            copy_tree(aaa, bbb)
            
            print ('\n\n.......Files Processed......Total Credit Card Records: '+str(len(records_list)))
            # for i in range(10,0,-1):
            #     time.sleep(100)
            #     print ('*')
            
            for file in glob.glob('*.xlsx'):
                oldName = file
                newName = file.replace("_-","-")
                os.rename(oldName, newName)
            
            del_file = glob.glob("L2CDZU*")
            for dem in del_file:
                os.remove(dem)
            
            with open("config/File_DupeCheck.csv",'r+') as dupecheck_file:
                date_now=int(datetime.datetime.now().strftime("%y%j"))
                dupecheck_file_filecontents = dupecheck_file.readlines()
                dupecheck_file.seek(0)
                for line in dupecheck_file_filecontents:
                    date_check = int(line.split(":")[0].rstrip())
                    
                    if (date_now-15)<date_check:
                        
                        dupecheck_file.write(line.rstrip()+"\n")
                for file in file_name:
                    print(file)
                    dupecheck_file.write(str(datetime.datetime.now().strftime("%y%j"))+":"+file+"\n")
                
                dupecheck_file.truncate()
            dupecheck_file.close()
                
            with open('config/BD_AWB.txt', 'r+') as bdfin:
                contents =  bdfin.readlines()
                bdremainingnew = len(contents[bd_num:])
                bdfin.seek(0)
                for line in contents[bd_num:]:
                    bdfin.write(line)
                bdfin.truncate()
            bdfin.close()
            
            with open('config/DL_AWB.txt', 'r+') as dlfin:
                contents =  dlfin.readlines()
                dtremainingnew = len(contents[dl_num:])
                dlfin.seek(0)
                for line in contents[dl_num:]:
                    dlfin.write(line)
                dlfin.truncate()
            dlfin.close()
            
           
            with open('config/IP_AWB.txt', 'r+') as ipfin:
                contents =  ipfin.readlines()
                ipremainingnew = len(contents[ip_num:])
                ipfin.seek(0)
                for line in contents[ip_num:]:
                    ipfin.write(line)
                ipfin.truncate()
            ipfin.close()
                
            with open('AWB_REMAINING_COUNT_NEW.txt','w') as awb_count_new:
                awb_count_new.write('BD   : ' + str(bdremainingnew)+'\n'+'DTDC : '+str(dtremainingnew)+'\nIP   : '+str(ipremainingnew) )
                print('BD   : ' + str(bdremainingnew)+'\n'+'DTDC : '+str(dtremainingnew)+'\nIP   : '+str(ipremainingnew) )
            awb_count_new.close()
            
            
            with open('config/VETTA_PP_NUMBER.csv', 'r+') as vetta_pp_in:
                contents =  vetta_pp_in.readlines()
                vetta_remainingnew = len(contents[vetta_pp:])
                vetta_pp_in.seek(0)
                for line in contents[vetta_pp:]:
                    vetta_pp_in.write(line)
                vetta_pp_in.truncate()
            vetta_pp_in.close()
        
            
            with open('config/ZENITH_PP_NUMBER.csv', 'r+') as zenith_pp_in:
                contents = zenith_pp_in.readlines()
                zenith_remainingnew = len(contents[zenith_pp:])
                zenith_pp_in.seek(0)
                for line in contents[zenith_pp:]:
                    zenith_pp_in.write(line)
                zenith_pp_in.truncate()
                
            zenith_pp_in.close()
            
            with open('config/AUC_batch_series', 'r+') as batch_series_read:
                contents =  batch_series_read.readlines()
                batch_series_read.seek(0)
                for line in contents[1:]:
                    batch_series_read.write(line)
                batch_series_read.truncate()
            batch_series_read.close()
            
           
            
            with open('REMAINING_PP_COUNT_NEW.txt','w') as pp_count_new:
                pp_count_new.write('Remaining VETTA Count  : ' + str(vetta_remainingnew)+'\n'+'Remaining ZENITH Count : '+str(zenith_remainingnew)+'\n' )
                print('Remaining VETTA  Count  : ' + str(vetta_remainingnew)+'\n'+'Remaining ZENITH Count : '+str(zenith_remainingnew)+'\n')
            pp_count_new.close()
            
            with open('./config/AUF_CREDIT_PP_CONSOLE.txt','a') as file_write:
                for line in pp_num:
                    file_write.write(line+'\n')
                    
                    
            file_write.close()
            
            with open('config/Priority_Pass_Data_AUF_BANK.csv', 'a') as pp_file_auf_ha:
                for data in pp_list:
                    pp_file_auf_ha.write(data+"\n")
            pp_file_auf_ha.close()

        
    
except Exception as e:    
    traceback.print_exc()

ts = datetime.datetime.now()
ptime = ts.strftime("%d.%m.%Y_%H%M%S")
print(ptime)
 

closeInput = input("Press ENTER to exit")
print ("Closing...")    
            