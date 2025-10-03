# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 16:22:49 2020

@author: rajeev.jadaun
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
                    
                    print_exp_date_acc = line_acc[162:164]+'/'+line_acc[164:166]
                    pp_exp_date_acc = (ptime[3:5]+ptime[8:10])
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
                        varient = 'Purchase_Reward_Credit_Card'
                    elif c_bin_acc == '483974'  and  logo_acc == '702':
                        varient = 'Purchase_Credit_Card'
                    elif c_bin_acc == '483974'  and  logo_acc == '703':
                        varient = 'Secured_Purchase_Credit_Card'
                    
                    elif c_bin_acc == '483894'  and  logo_acc == '801':
                        varient = 'Business_Reward_Credit_Card'
                    elif c_bin_acc == '483894'  and  logo_acc == '802':
                        varient = 'Secured_Business_Credit_Card'
                    elif c_bin_acc == '483894'  and  logo_acc == '803':
                        varient = 'Business_Cashback_Credit_Card'
                    
                    
                   
                    #dateq=(date_acc[0:1]+'-'+month+'-'+(date_acc[4:5])
                              
                    file_credit_card_ff_acc = ' '+'|'+c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+ref_number+'|'+card_type+'|'+mask_pan_acc+'|'+account_number_acc+'|'+card_action+'|'+salutation_acc+'|'+mailer_name_acc+'|'+mailer_address1_acc+'|'+mailer_address2_acc+'|'+mailer_address3_acc+'|'+mailer_address4_acc+'|'+mailer_city_acc+'|'+mailer_state_code_acc+'|'+mailer_postal_code_acc+'|'+mailer_mob_acc+'|'+customer_id_acc+'|'+cr_card_limit+'|'+billing_cycle+'|'+superscript+'|'+print_card_holder_name_acc+'|'+pct_id+'|'#+jdtodatestd(date_acc)
                    file_credit_card_em_acc = line_acc[:]
                
                    bin_list.append(c_bin_acc+logo_acc+gender_code_acc)
                    bin_list = list(dict.fromkeys(bin_list))
                    qty = ''
   
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
                    product = 'Purchase_Reward_Credit_Card'
                elif c_bin_acc == '483974'  and  logo_acc == '702':
                    product = 'Purchase_Credit_Card'
                elif c_bin_acc == '483974'  and  logo_acc == '703':
                    varient = 'Secured_Purchase_Credit_Card'
                
                elif c_bin_acc == '483894'  and  logo_acc == '801':
                    product = 'Business_Reward_Credit_Card'
                elif c_bin_acc == '483894'  and  logo_acc == '802':
                    product = 'Secured_Business_Credit_Card'
                elif c_bin_acc == '483894'  and  logo_acc == '803':
                    product = 'Business_Cashback_Credit_Card'
                #ADDITONAL DETAIL FOR ADD CARDS
                ps1 = account_number_acc+'|'+card_type+'|'+mask_pan_acc+'|'+card_action+'|'+c_bin_f_acc+'|'+logo_acc+'|' +gender_code_acc+'|'+varient+'|'+mailer_name_acc
                
                with open('AUC_EM_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+str(product)+'_'+celeb+'_'+str(ptime)+'.txt', 'a') as em_file_acc:
                    em_file_acc.write(file_credit_card_em_acc)
                em_file_acc.close()
                
                
                with open('AUF_FF_MIS_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+str(product)+'_'+celeb+'_'+str(ptime)+'.txt', 'a') as ff_file_acc:
                     ff_file_acc.write(file_credit_card_ff_acc +'\n')
                ff_file_acc.close()   
                
                with open('AUF_FF_MIS_MERGE_'+str(ptime)+'.txt', 'a') as ff_file_accm:
                    date_q=jdtodatestd(date_acc)
                    date_q=str(date_q)    
                    ff_file_accm.write(file_credit_card_ff_acc+date_q+'\n')
                ff_file_accm.close()
                
                ps_list.append(ps)
                ps1_list.append(ps1)
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
                    pp_cardnumber_acc = pp_cardnumber_acc+'0'+ax[0:1]
                    
                #if card_holder_type_acc == '1':
                track1_acc = '%PP/'+salutation_acc+'/'+print_card_holder_name_acc+'//''?'
                #elif card_holder_type_acc == '0':
                #    track1_acc = '%PP/'+salutation_acc+'/'+mailer_name1_acc+' '+mailer_name2_acc+'//'+mailer_name3_acc+'?'
  
                #track2_acc = ';'+pp_cardnumber_acc+'='+ line_acc[162:164]+'20'+line_acc[164:166] +'?'
                #new track 2 as per customer requirement change expiry 3 years from date of processing
                track2_acc = ';'+pp_cardnumber_acc+'='+ (pp_exp_date_acc[0:2]+'20'+str(int(pp_exp_date_acc[2:4])+3)) +'?'
                
                file_pp = '#0#'+mask_pan_acc+'#1#'+pp_cardnumber_acc+'#2#'+track1_acc+'#3#'+track2_acc+'#4#'+(pp_exp_date_acc[0:2]+'/'+str(int(pp_exp_date_acc[2:4])+3))+'#5#'+salutation_acc+' '+print_card_holder_name_acc+'#6#'
                file_pp_merge = account_number_acc+'|'+ref_number+'|'+mask_pan_acc+'|'+salutation_acc+' '+print_card_holder_name_acc+'|'+pp_cardnumber_acc+'|'+(pp_exp_date_acc[0:2]+'/'+str(int(pp_exp_date_acc[2:4])+3))+'|'+varient+'|'+logo_acc+'|'+gender_code_acc
                auf_pp_output = account_number_acc+','+logo_acc+','+mask_pan_acc+','+card_holder_name_acc.rstrip()+','+card_action+','+pp_cardnumber_acc+','+str(ptime[0:10])
                '''
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
                            with open('AUF_PP_MERGE_'+str(ptime)+'.txt', 'a') as pp_file_m:
                                pp_file_m.write(file_pp_merge +'\n')
                                #print (file_pp_merge)
                            pp_file_m.close()        
                
        
                if (c_bin_acc == '465523' or c_bin_acc == '457036'):
                    if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                        if mask_pan_acc not in filecontents:
                            with open('Priority_Pass_Data_'+str(ptime[0:10])+'.csv', 'a') as pp_file_auf:
                                pp_file_auf.write(auf_pp_output +'\n')
                                
                            pp_file_auf.close()
                    
                '''
                #WITHOUT ADD ON PP CARD OF VETTA VARIANT
                if ((c_bin_acc == '465523' and card_holder_type_acc=='1')   or c_bin_acc == '457036'):
                    if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A' ):
                        if mask_pan_acc not in filecontents:
                            with open('AUC_PP_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+product+'_'+str(ptime)+'EM.txt', 'a') as pp_file:
                                pp_file.write(file_pp +'\n')
                                #print (file_pp)
                            pp_file.close()
                        
                if ((c_bin_acc == '465523' and card_holder_type_acc=='1') or c_bin_acc == '457036'):
                    if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                        if mask_pan_acc not in filecontents:
                            with open('AUF_PP_MERGE_'+str(ptime)+'.txt', 'a') as pp_file_m:
                                pp_file_m.write(file_pp_merge +'\n')
                                #print (file_pp_merge)
                            pp_file_m.close()        
                
        
                if ((c_bin_acc == '465523' and card_holder_type_acc=='1') or c_bin_acc == '457036'):
                    if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                        if mask_pan_acc not in filecontents:
                            with open('Priority_Pass_Data_'+str(ptime[0:10])+'.csv', 'a') as pp_file_auf:
                                pp_file_auf.write(auf_pp_output +'\n')
                                
                            pp_file_auf.close()
                            
                #extra files for add on pp of vetta varient for cross checking
                if ((c_bin_acc == '465523' and card_holder_type_acc=='0') ):
                    if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A' ):
                        if mask_pan_acc not in filecontents:
                            with open('1_DELETEFILE_AUF_PP_B'+str(c_bin_acc)+'_L'+str(logo_acc)+'_G'+str(gender_code_acc)+'_'+product+'_'+str(ptime)+'.txt', 'a') as pp_file:
                                pp_file.write(file_pp +'\n')
                                #print (file_pp)
                            pp_file.close()
                        
                if ((c_bin_acc == '465523' and card_holder_type_acc=='0') ):
                    if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                        if mask_pan_acc not in filecontents:
                            with open('1_DELETEFILE_AUF_PP_MERGE_'+str(ptime)+'.txt', 'a') as pp_file_m:
                                pp_file_m.write(file_pp_merge +'\n')
                                #print (file_pp_merge)
                            pp_file_m.close()        
                
        
                if ((c_bin_acc == '465523' and card_holder_type_acc=='0')):
                    if (card_action_code == '1' or card_action_code == '2' or card_action_code == '7' or card_action_code == 'A'):
                        if mask_pan_acc not in filecontents:
                            with open('1_DELETEFILE_Priority_Pass_Data_'+str(ptime[0:10])+'.csv', 'a') as pp_file_auf:
                                pp_file_auf.write(auf_pp_output +'\n')
                                
                            pp_file_auf.close()
                #extra files for add on pp of vetta varient for cross checking
                #Alert for new bin -483974
                if (c_bin_acc == '483974' ):
                    with open('ALERT!!___NEW BIN 483974 RECEIVED.dat', 'a') as alert_ff:
                        alert_ff.write(c_bin_f_acc+'|'+logo_acc+'|'+gender_code_acc+'|'+varient+'|'+ref_number+'|'+card_type+'|'+mask_pan_acc+'|'+account_number_acc+'|'+card_action+'\n')
                    alert_ff.close()
                    
                
                
                
outfile_acc.close()  

for idx, val in enumerate(ps_list):
            #print(idx, val)
            acc_card_count = (ps_list.count(ps_list[idx]))
            if ps_list[idx][17:] == 'Primary Card':
                p_acc_card_count.append(str(ps_list[idx])+'|'+str(ps_list.count(ps_list[idx])))
            if ps_list[idx][17:] == 'Add-on  Card':
                s_acc_card_count.append(str(ps_list[idx])+'|'+str(ps_list.count(ps_list[idx])))

with open('PrimaryCard_detail_'+str(ptime)+'.txt', 'w') as ps_d:
  ps_d.writelines(["%s\n" % item  for item in p_acc_card_count])
ps_d.close()
with open('del_SecondaryCard.txt', 'w') as ps_d:
  ps_d.writelines(["%s\n" % item  for item in s_acc_card_count])
  for oni in s_acc_card_count:
      print ((oni))
ps_d.close()

uniqlines = set(open('del_SecondaryCard.txt').readlines())
bar = open('SecondaryCard_details_'+str(ptime)+'.txt', 'w').writelines(set(uniqlines))


for idx, val in enumerate(ps1_list):
    #print(idx, val)
    acc_card_count1 = (ps1_list.count(ps1_list[idx]))
    # if ps_list[idx][17:] == 'Primary Card':
    # p_acc_card_count.append(str(ps_list[idx])+'|'+str(ps_list.count(ps_list[idx])))
    if ps_list[idx][17:29] == 'Add-on  Card':
        s_acc_card_count1.append(
            str(ps1_list[idx])+'|'+str(ps1_list.count(ps1_list[idx])))

with open('del_SecondaryCard1.txt', 'w') as ps_d:
    ps_d.writelines(["%s\n" % item for item in s_acc_card_count1])
    # for oni in s_acc_card_count1:
    #print ((oni))
ps_d.close()

uniqlines = set(open('del_SecondaryCard1.txt').readlines())
bar = open('SecondaryCard_updated_details_'+str(ptime) +
           '.txt', 'w').writelines(set(uniqlines))


from collections import defaultdict
d1 = defaultdict(list)
for k, v in pps_list:
    d1[k].append(v)
d = dict((k, tuple(v)) for k, v in d1.items())
for key, value in d.items():
    res = str(value)[1:-1]    
    print(key, ' : ', res)

del_file1 = glob.glob("del*")
for de in del_file1:   
    os.remove(de)
    
del_file2 = glob.glob("*account*")
for del2 in del_file2:   
    os.remove(del2)
    
del_file = glob.glob("merge*")
for dem in del_file:   
    os.remove(dem)
    
    
del_file = glob.glob("L2CDZU*")
for deml in del_file:   
    os.remove(deml)

for i,k in enumerate(file_name):
    result = hashlib.md5(file_name[i].encode())
    filenamehash = result.hexdigest()
    filenamehash = str(filenamehash)
    print (file_name[i]+'---'+filenamehash)
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
for fn in glob.glob('*AUC*.txt'):
    with open(fn) as f:
        names[fn]=sum(1 for file_count in f if file_count.strip() and not file_count.startswith('~'))       
with open('AUF_FILE_COUNT_'+str(ptime)+'.csv', 'w') as f:
    f.write('File Name,File Count,Non-Replace,Replace'+'\n')
    [f.write('{0},{1}\n'.format(key, value)) for key, value in names.items()] 

from prettytable import PrettyTable
ptx = PrettyTable()
ptx.field_names = ["Bin", "Artwork No.","JB No.", "EMBOSS Filename","Qty", "Job setup", "Method -Ribbon/Foil"]

for key, value in names.items():
    if key[4:46] == 'EM_B457036_L401_G1_Zenith_CII_Young_Indian':
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
        dg_color = 'DG-White'
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
    if key[4:46] == 'EM_B457036_L401_G1_Zenith_CII_Young_Indian':
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
        dg_color = 'DG-White'
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
                
    ptx1.add_row([key,"","","","",""])
ptx1.align = "c"
ptd1=ptx1.get_string()

datedmy = str(x)[8:10]+'-'+str(x)[5:7]+'-'+str(x)[0:4]
with open('AUF_CREDIT_BATCHCARD_'+str(ptime)+'.dat', 'w') as file:
  file.write('                                                '+'BANKING PERSONALISATION BATCH CARD'+'                              '+'Date: '+ptime[0:10]+'\n')
  file.write('                                                       AUC-'+ptime[0:10]+'-'+batch_number+'                                    '+'AUF CREDIT PROJECT(DI)\n\n')
  #file.write('EMBOSS FILE NAME: SBM_EMBOSS_'+str(x)+'_'+str(qty)+'.txtt\n')
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



print ('\n\n.......Files Processed......Total Credit Card Records: '+str(len(records_list)))
# for i in range(10,0,-1):
#     time.sleep(100)
#     print ('*')