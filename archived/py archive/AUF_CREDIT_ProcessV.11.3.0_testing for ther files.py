# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 17:30:15 2022

@author: rajeev.jadaun
"""

#    # -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 16:22:49 2020

@author: rajeev.jadaun
      AUF_CREDIT_ProcessV.11.3.0.py:11-01-2022[Full automation]
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
pps_list = []
p_acc_card_count =[]
s_acc_card_count = []
pp_dup_check =[]
bd_num=0
dl_num=0
ip_num=0
awb_number_bd = []
awb_number_dl = []
awb_number_ip = []
ts = datetime.datetime.now()
ptime = ts.strftime("%d.%m.%Y_%H%M%S")
count=0
with open('config/AUC_batch_series', 'r') as fin:
    batch_series_data = fin.read().splitlines(True)
    batch_series = batch_series_data[0:1]
with open('config/AUC_batch_series', 'w') as fout:
    fout.writelines(batch_series_data[1:])
listToStr = ' '.join([str(elem) for elem in batch_series])
batch_number = listToStr[0:5]

with open('config/BD_AWB.txt', 'r') as bdfin,open('config/BD_AWB_USING.txt', 'w') as bdfout:
    contents= bdfin.readlines()
    bdfout.writelines(contents)
with open('config/DL_AWB.txt', 'r') as dtfin,open('config/DL_AWB_USING.txt', 'w') as dtfout:
    contents= dtfin.readlines()
    dtfout.writelines(contents)    
with open('config/IP_AWB.txt', 'r') as ipfin,open('config/IP_AWB_USING.txt', 'w') as ipfout:
    contents= ipfin.readlines()
    ipfout.writelines(contents)
    
    
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
    datestd=str(datestd)
    
    if datestd[5:7] == '01':
        month = 'Jan'
    elif datestd[5:7] == '02':
        month = 'Feb'
    elif datestd[5:7] == '03':
        month = 'Mar'
    elif datestd[5:7] == '04':
        month = 'Apr'
    elif datestd[5:7] == '06':
        month = 'May'
    elif datestd[5:7] == '07':
        month = 'Jun'
    elif datestd[5:7] == '08':
        month = 'Jul'
    elif datestd[5:7] == '09':
        month = 'Aug'
    elif datestd[5:7] == '10':
        month = 'Oct'
    elif datestd[5:7] == '11':
        month = 'Nov'
    elif datestd[5:7] == '12':
        month = 'Dec'
    
    plastic_issue_date=(datestd[8:10]+'-'+month+'-'+datestd[0:4])
    return(plastic_issue_date)  
count=0
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
                    f_bin_acc = line_acc[9:15]
                    pp1_acc = line_acc[18:25]
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
                    
#--------------------------pp dup check--------------------------  L
                  #  with open('config/pp_db', 'a') as pp_dup:
                  #      pp_dup.write(ppnum7+'\n')
                  #  pp_dup.close()    
                    
                    
#-----------------------------------------------------------------------------------------
                    
                    
                    
                    
                    
                    pp_cardnumber_acc = c_bin_acc+'999'+str(ppnum7)
                    
                    print_exp_date_acc = line_acc[162:164]+'/'+line_acc[164:166]
                    gender_code_acc = line_acc[2103:2104]
                    customer_id_acc1 = line_acc[1134:1153].lstrip()
                    customer_id_acc = customer_id_acc1.rstrip()
                    cr_card_limit = line_acc[167:182]
                    card_action_code = line_acc[150:151]
                    billing_cycle = line_acc[3844:3846]
                    billing_cycle_int = int(billing_cycle)
                    
                    if gender_code_acc == '1':
                        salutation_acc ='Mr.'
                    elif gender_code_acc =='2':
                        salutation_acc = 'Ms.'
                    else:
                        salutation_acc ='Not Found'

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
                    j_day=str(j_p)

                    ref_number = customer_id_acc[2:]+card_holder_name_acc[0:4].upper()+j_day[4:7]+j_day[0:4]+str(s_no)
                    if card_holder_type_acc == '1':
                        card_type = 'Primary Card'
                    elif card_holder_type_acc == '0':
                        card_type = 'Add-on  Card'
                    
                    ps = account_number_acc+'|'+card_type
                    pps  = [account_number_acc, mask_pan_acc]
                    
                    
                    if c_bin_acc == '466505'  and  logo_acc == '101': 
                        if plastic_id == '          ':
                            varient = 'Altura'
                        elif plastic_id == '0000000002':
                            varient = 'Altura Celeb Male'
                        elif plastic_id == '0000000003':
                            varient = 'Altura Celeb Female'
                        else:
                            varient ='Not Found'
                        
                    if c_bin_acc == '466505'  and  logo_acc == '102':
                        if gender_code_acc == '0':
                            varient = 'AlturaPlusBlue'
                        elif gender_code_acc == '1':
                            varient = 'AlturaPlusBlue'
                        elif gender_code_acc == '2':
                            varient = 'AlturaPlusRuby'
                    if c_bin_acc == '465523'  and  logo_acc == '301': 
                        varient = 'Vetta'
                    if c_bin_acc == '457036'  and  logo_acc == '401': 
                        varient = 'Zenith'
                    
                    if logo_acc=='101' and pct_id=='101':
                        joining_fees='NIL'
                        annual_fees='NIL'
                    elif logo_acc=='101' and pct_id=='001':
                        joining_fees='199'
                        annual_fees='199'
                    elif logo_acc=='101' and pct_id=='102':
                        joining_fees='NIL'
                        annual_fees='199'
                    
                    elif logo_acc=='102' and pct_id=='103':
                        joining_fees='NIL'
                        annual_fees='NIL'
                    elif logo_acc=='102' and pct_id=='003':
                        joining_fees='499'
                        annual_fees='499'
                    elif logo_acc=='102' and pct_id=='104':
                        joining_fees='NIL'
                        annual_fees='499'
                    
                    elif logo_acc=='103' and pct_id=='015':
                        joining_fees='45'
                        annual_fees='45'
                    
                    elif logo_acc=='301' and pct_id=='105':
                        joining_fees='NIL'
                        annual_fees='NIL'
                    elif logo_acc=='301' and pct_id=='007':
                        joining_fees='2,999'
                        annual_fees='2,999'
                    elif logo_acc=='301' and pct_id=='106':
                        joining_fees='NIL'
                        annual_fees='2,999'
                    
                    elif logo_acc=='302' and pct_id=='110':
                        joining_fees='NIL'
                        annual_fees='NIL'
                    elif logo_acc=='302' and pct_id=='009':
                        joining_fees='1,499'
                        annual_fees='1,499'
                    elif logo_acc=='302' and pct_id=='020':
                        joining_fees='749'
                        annual_fees='749'
                    elif logo_acc=='302' and pct_id=='021':
                        joining_fees='2,999'
                        annual_fees='2,999'
                    elif logo_acc=='302' and pct_id=='010':
                        joining_fees='NIL'
                        annual_fees='1,499'
                    elif logo_acc=='302' and pct_id=='018':
                        joining_fees='NIL'
                        annual_fees='749'
                    elif logo_acc=='302' and pct_id=='019':
                        joining_fees='NIL'
                        annual_fees='2,999'
                        
                    elif logo_acc=='303' and pct_id=='022':
                        joining_fees='99'
                        annual_fees='99'
                    elif logo_acc=='303' and pct_id=='111':
                        joining_fees='NIL'
                        annual_fees='NIL'
                    
                    elif logo_acc=='401' and pct_id=='107':
                        joining_fees='NIL'
                        annual_fees='NIL'
                    elif logo_acc=='401' and pct_id=='011':
                        joining_fees='7,999'
                        annual_fees='7,999'
                    elif logo_acc=='401' and pct_id=='108':
                        joining_fees='NIL'
                        annual_fees='7,999'
                    
                    #jdate=str(date_acc)
                    #datestd = datetime.datetime.strptime(jdate, '%Y%j' ).date()
                    
                 
                
                    #dateq=(date_acc[0:1]+'-'+month+'-'+(date_acc[4:5])
                              
                    file_credit_card_ff_acc = ' '+'|'+c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+ref_number+'|'+card_type+'|'+mask_pan_acc+'|'+account_number_acc+'|'+card_action+'|'+salutation_acc+'|'+mailer_name_acc+'|'+mailer_address1_acc+'|'+mailer_address2_acc+'|'+mailer_address3_acc+'|'+mailer_address4_acc+'|'+mailer_city_acc+'|'+mailer_state_code_acc+'|'+mailer_postal_code_acc+'|'+mailer_mob_acc+'|'+customer_id_acc+'|'+cr_card_limit+'|'+billing_cycle+'|'+superscript+'|'+print_card_holder_name_acc+'|'+pct_id+'|'#+jdtodatestd(date_acc)
                    
                    file_credit_card_ff_acc_test_1 = ' '+'|'+account_number_acc+'|'+mask_pan_acc+'|'+mailer_name_acc+'|'+'|'+'|'+'|'+'|'
                    
                    file_credit_card_ff_acc_test_3=card_action+'|'+'|'+'|'+'|'+c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+mailer_address1_acc+'|'+mailer_address2_acc+'|'+mailer_address3_acc+'|'+mailer_address4_acc+'|'+mailer_city_acc+'|'+mailer_state_code_acc+'|'+mailer_postal_code_acc+'|'+mailer_mob_acc+'|'+customer_id_acc+'|'+cr_card_limit+'|'+billing_cycle+'|'+superscript+'|'+print_card_holder_name_acc+'|'+joining_fees+'|'+annual_fees+'|'+str(jdtodatestd(date_acc))
                    
                    file_credit_card_ff_acc_new = ' '+'|'+account_number_acc+'|'+ref_number+'|'+mask_pan_acc+'|'+salutation_acc+' '+mailer_name_acc+'|'+pp_cardnumber_acc+'|'+print_exp_date_acc+'|'+varient+'|'+logo_acc+'|'+gender_code_acc#+jdtodatestd(date_acc)
                    file_credit_card_em_acc = line_acc[:]
                    header='Sr. No|Account Number|Primary Card number|Customer Name|Add-on Card 1|Add-on Card 2|Add-on Card 3|Add-on Card 4|PP  Card No_Primary|PP  Card No_Addon1|PP  Card No_Addon2|PP  Card No_Addon3|Ref no.|AWB. No.|Courier|Courier Code|Card Action|Primary Count|Add-on Count|Total Cards|Bin|Logo|Gender Code|Varient|Address Line 1|Address Line 2|Address Line 3|Address Line 4|City|State Code|Postal Code|Mobile Number|Cust Unique ID|Credit Limit|Statement Date |Extention|Embo_Name|Joining Fees|Annual Fees|Card Issuance Date'
                    bin_list.append(c_bin_acc+logo_acc+gender_code_acc)
                    bin_list = list(dict.fromkeys(bin_list))
                    qty = ''
                    
                    
                #ASSIGNING COURIER
                with open('config/PINCODE_MASTER.csv', 'r') as pin:
                    routing_codewe=pin.readlines() 
                    flag = 0 

                    routing_code=''
                    customer_code=''
                    for line in routing_codewe:
                        pincodedata=line.split(',')
                        if mailer_postal_code_acc!='':
                            if  mailer_postal_code_acc in pincodedata[0]:# and pincodedata[4]=='BLUEDART':
                                flag=1
                                
                                courier=pincodedata[2].rstrip()
                                routing_code=pincodedata[1].rstrip()
                                break
                    if flag == 0 :
                        
                        courier='Speedpost'
                        routing_code='921-417'
                        courier=str(courier)   
                pin.close()
                
                
                if courier == 'BLUEDART':
                    with open('config/BD_AWB_USING.txt', 'r') as bdfin:
                        bdawb1 = bdfin.readlines()
                        awb_number=bdawb1[bd_num].rstrip()
                        bd_num=bd_num+1
                        awb_number_bd=bdawb1[bd_num:]
                        #print(awb_number_bd)
                        #print(awb_number)
                       
                elif courier == 'DELHIVERY':
                    with open('config/DL_AWB_USING.txt', 'r') as dlfin:
                        dlawb = dlfin.readlines()
                        awb_number=dlawb[dl_num].rstrip()
                        dl_num=dl_num+1
                        awb_number_dl=dlawb[dl_num:]
                        
                     
                elif courier == 'Speedpost':
                    with open('config/IP_AWB_USING.txt', 'r') as ipfin:
                        ipawb = ipfin.readlines()
                        awb_number=ipawb[ip_num].rstrip()
                        ip_num=ip_num+1
                        awb_number_ip=ipawb[ip_num:]
                        
                        
                if c_bin_acc == '466505'  and  logo_acc == '101': 
                    product = 'Altura'
                if c_bin_acc == '466505'  and  logo_acc == '102':
                    if gender_code_acc == '0':
                        product = 'AlturaPlusBlue'
                    elif gender_code_acc == '1':
                        product = 'AlturaPlusBlue'
                    elif gender_code_acc == '2':
                        product = 'AlturaPlusRuby'
                if c_bin_acc == '465523'  and  logo_acc == '301': 
                    product = 'Vetta'
                if c_bin_acc == '457036'  and  logo_acc == '401': 
                    product = 'Zenith'
                    
                
                with open('AUC_EM_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+str(product)+'_'+celeb+'_'+str(ptime)+'.txt', 'a') as em_file_acc:
                    em_file_acc.write(file_credit_card_em_acc)
                em_file_acc.close()
                
                
                with open('xxAUC_FF_MIS_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+str(product)+'_'+celeb+'_'+str(ptime)+'.txt', 'a') as ff_file_acc:
                     ff_file_acc.write(file_credit_card_ff_acc +awb_number+'|'+routing_code+'|'+courier+'\n')
                ff_file_acc.close()   
                
                  
                
                
                with open('xxAUF_FF_MIS_MERGE_'+str(ptime)+'.txt', 'a') as ff_file_accm:
                    date_q=jdtodatestd(date_acc)
                    date_q=str(date_q)
                    
                    ff_file_accm.write(file_credit_card_ff_acc+awb_number+'|'+routing_code+'|'+courier+date_q+'\n')
                    
                ff_file_accm.close()
                
                ps_list.append(ps)
                pps_list.append(pps)
                
                cardnumber_list.append(cardnumber_acc)
                
                if card_holder_type_acc == '1':
                    pp_cardnumber_acc = pp_cardnumber_acc+'01'
                    primary_card.append(cardnumber_acc)
                
                if card_holder_type_acc =='0':
                    secondary_card.append(cardnumber_acc)
                    
                if (card_holder_type_acc == '0'):
                    card_count = len(secondary_card)
                    r = (range(2, (card_count+1))) 
                    cc = card_count+1
                    
                    for j in range(cc+1):
                        ax= str(j)
                    pp_cardnumber_acc = pp_cardnumber_acc+'0'+ax
                    
                #if card_holder_type_acc == '1':
                track1_acc = '%PP/'+salutation_acc+'/'+print_card_holder_name_acc+'//''?'
                #elif card_holder_type_acc == '0':
                #    track1_acc = '%PP/'+salutation_acc+'/'+mailer_name1_acc+' '+mailer_name2_acc+'//'+mailer_name3_acc+'?'
  
                track2_acc = ';'+pp_cardnumber_acc+'='+ line_acc[162:164]+'20'+line_acc[164:166] +'?'
                
                file_credit_card_ff_acc_test_2=pp_cardnumber_acc+'|'+'|'+'|'+'|'+ref_number+'|'+awb_number+'|'+courier+'|'+routing_code+'|'
                
                
                file_pp = '#0#'+mask_pan_acc+'#1#'+pp_cardnumber_acc+'#2#'+track1_acc+'#3#'+track2_acc+'#4#'+print_exp_date_acc+'#5#'+salutation_acc+' '+print_card_holder_name_acc+'#6#'
                file_pp_merge = account_number_acc+'|'+ref_number+'|'+mask_pan_acc+'|'+salutation_acc+' '+print_card_holder_name_acc+'|'+pp_cardnumber_acc+'|'+print_exp_date_acc+'|'+varient+'|'+logo_acc+'|'+gender_code_acc
                auf_pp_output = account_number_acc+','+logo_acc+','+mask_pan_acc+','+card_holder_name_acc.rstrip()+','+card_action+','+pp_cardnumber_acc+','+str(ptime[0:10])
                
                
                with open('xxAUC_FF_MIS_test_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+str(product)+'_'+celeb+'_'+str(ptime)+'.txt', 'a') as ff_file_acc:
                    #if count==0:
                        #ff_file_accm.write(header)
                    #ff_file_acc.write('Sr. No|Account Number|Primary Card number|Customer Name|Add-on Card 1|Add-on Card 2|Add-on Card 3|Add-on Card 4|PP  Card No_Primary|PP  Card No_Addon1|PP  Card No_Addon2|PP  Card No_Addon3|Ref no.|AWB. No.|Courier|Courier Code|Card Action|Primary Count|Add-on Count|Total Cards|Bin|Logo|Gender Code|Varient|Address Line 1|Address Line 2|Address Line 3|Address Line 4|City|State Code|Postal Code|Mobile Number|Cust Unique ID|Credit Limit|Statement Date |Extention|Embo_Name|Joining Fees|Annual Fees|Card Issuance Date\n')
                    ff_file_acc.write(file_credit_card_ff_acc_test_1+file_credit_card_ff_acc_test_2+file_credit_card_ff_acc_test_3+'\n')
                    
                ff_file_acc.close() 
                
                if (c_bin_acc == '465523' or c_bin_acc == '457036'):
                    if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                        if mask_pan_acc not in filecontents:
                            with open('AUC_PP_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+product+'_'+str(ptime)+'EM.txt', 'a') as pp_file:
                                pp_file.write(file_pp +'\n')
                                #print (file_pp)
                            pp_file.close()
                
                if (c_bin_acc == '465523' or c_bin_acc == '457036'):
                    if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                        if mask_pan_acc not in filecontents:
                            with open('xxAUC_PP_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+product+'_'+str(ptime)+'.csv', 'a') as pp_file:
                                #if count ==0:
                                    #pp_file.write('Sr. No|Account Number|Ref no.|Primary Card number|Customer Name|PP  Card No_Primary|Expiry Date|Variant|Logo|Gender|AWB. No.|Courier\n')
                                pp_file.write('Sr. No|Account Number|Ref no.|Primary Card number|Customer Name|PP  Card No_Primary|Expiry Date|Variant|Logo|Gender|AWB. No.|Courier\n')
                                pp_file.write(file_credit_card_ff_acc_new+'|' +awb_number+'|'+courier+'|'+routing_code+'\n')
                                #print (file_pp)
                                count+=1
                            pp_file.close()
                            
                if (c_bin_acc == '465523' or c_bin_acc == '457036'):
                    if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                        if mask_pan_acc not in filecontents:
                            with open('AUC_PP_MERGE_'+str(ptime)+'.txt', 'a') as pp_file_m:
                                pp_file_m.write(file_pp_merge +'\n')
                                #print (file_pp_merge)
                            pp_file_m.close()        
                
        
                if (c_bin_acc == '465523' or c_bin_acc == '457036'):
                    if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                        if mask_pan_acc not in filecontents:
                            with open('Priority_Pass_Data_'+str(ptime[0:10])+'.csv', 'a') as pp_file_auf:
                                if count ==0:
                                    pp_file_auf.write('')
                                    
                                pp_file_auf.write(auf_pp_output +'\n')
                             
                            pp_file_auf.close() 
    
    with open('config/BD_AWB.txt', 'w') as bdfout:
        bdfout.writelines(awb_number_bd)
                
    with open('config/DL_AWB.txt', 'w') as dlfout:
        dlfout.writelines(awb_number_dl)
        
    with open('config/IP_AWB.txt', 'w') as ipfout:
        ipfout.writelines(awb_number_ip)
outfile_acc.close()  



del_file1 = glob.glob("del*")
for de in del_file1:   
    os.remove(de)
    
del_file2 = glob.glob("*account*")
for del2 in del_file2:   
    os.remove(del2)
    
del_file = glob.glob("merge*")
for dem in del_file:   
    os.remove(dem)
