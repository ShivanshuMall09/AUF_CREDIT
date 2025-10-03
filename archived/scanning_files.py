import glob
import pandas as pd
import os

Primary_Card_count = ''
files = glob.glob('AUF_CREDIT_SCANNING_CARD_FILE_*.csv')
Srn = 0
for file in files:
    
    addon_count =0
    previous_Primary_Card_number =''
    previous_Addon_Card_1 = ''
    previous_Addon_Card_2 = ''
    previous_Addon_Card_3 = ''
    previous_Addon_Card_4 = ''
    previous_PP_Card_No_Primary = ''
    previous_PP_Card_No_Addon1 = ''
    previous_PP_Card_No_Addon2 = ''
    previous_PP_Card_No_Addon3 = ''
    with open(file,'r') as infile,open('xAUF_CREDIT_SCANNING_CARD_FILE.txt','a') as outfile:
        contents = infile.readlines()
        size = len(contents)
        for ln in contents:
            val = ln.split('|')
            Account_Number       =val[1].strip() 
            Primary_Card_number  =val[2].strip()
            Customer_Name        =val[3].strip()
            Addon_Card_1         =val[4].strip()
            Addon_Card_2          =val[5].strip()
            Addon_Card_3         =val[6].strip()
            Addon_Card_4         =val[7].strip()
            PP_Card_No_Primary   =val[8].strip()
            PP_Card_No_Addon1    =val[9].strip()  
            PP_Card_No_Addon2    =val[10].strip()
            PP_Card_No_Addon3    =val[11].strip()
            Refno                =val[12].strip()
            AWB_No               =val[13].strip()
            Courier              =val[14].strip()
            Courier_Code         =val[15].strip()
            Card_Action          =val[16].strip()
            Primary_Count        =val[17].strip()
            Addon_Count          =val[18].strip()
            Total_Cards          =val[19].strip()
            Bin                  =val[20].strip()
            Logo                 =val[21].strip()
            Gender_Code          =val[22].strip()
            Varient              =val[23].strip()
            Address_Line_1       =val[24].strip()
            Address_Line_2       =val[25].strip()
            Address_Line_3       =val[26].strip()
            Address_Line_4       =val[27].strip()
            City                 =val[28].strip()
            State_Code           =val[29].strip()
            Postal_Code          =val[30].strip()
            Mobile_Number        =val[31].strip()
            Cust_Unique_ID       =val[32].strip()
            Total_PP_Count       =val[33].strip()
            Joining_Fees         =val[34].strip()
            Annual_Monthly_Fees  =val[35].strip()
            Card_Issuance_Date   =val[36].strip()
            CARDHOLDER_EMBOSSA_2 =val[37].strip()
            PLASTIC_ID           =val[38].strip()

            if(Primary_Card_number != ''):
                previous_Primary_Card_number = Primary_Card_number
            if(Addon_Card_1 != ''):
                previous_Addon_Card_1 = Addon_Card_1
                addon_count +=1
            if(Addon_Card_2 != ''):
                previous_Addon_Card_2 = Addon_Card_2
                addon_count +=1
            if(Addon_Card_3 != ''):
                previous_Addon_Card_3 = Addon_Card_3
                addon_count +=1
            if(Addon_Card_4 != '') :
                previous_Addon_Card_4 = Addon_Card_4
                addon_count +=1
            if(PP_Card_No_Primary != ''):
                previous_PP_Card_No_Primary = PP_Card_No_Primary
            if(PP_Card_No_Addon1 != ''):
                previous_PP_Card_No_Addon1 = PP_Card_No_Addon1
            if(PP_Card_No_Addon2 != ''):
                previous_PP_Card_No_Addon2 = PP_Card_No_Addon2
            if(PP_Card_No_Addon2 != ''):
                previous_PP_Card_No_Addon3 = PP_Card_No_Addon2
            if previous_Primary_Card_number == '':
                Primary_Card_count = '0'    
            else:
                    Primary_Card_count = '1' 
        Srn +=1
        outfile.write(str(Srn).zfill(4)+'|'+Account_Number+'|'+previous_Primary_Card_number+'|'+previous_Addon_Card_1+'|'+previous_Addon_Card_2+'|'+previous_Addon_Card_3+'|'+previous_Addon_Card_4+'|'+previous_PP_Card_No_Primary+'|'+previous_PP_Card_No_Addon1+'|'+previous_PP_Card_No_Addon2+'|'+previous_PP_Card_No_Addon3+'|'+AWB_No+'|'+Courier+'|'+Primary_Card_count+'|'+str(addon_count)+'|'+str(size)+'|'+Bin+'|'+Logo+'|'+Gender_Code+'|'+Varient+'\n')
                 
    
with open('xAUF_CREDIT_SCANNING_CARD_FILE.txt','r') as infile,open('AUF_CREDIT_SCANNING_CARD_FILE.csv','a') as scan_file:
    contents = infile.readlines()
    scan_file.write('Sr. No.|Account Number|Primary Card Number|Addon card 1|Addon card 2|Addon card 3|Addon card 4|PP Card No Primary|PP Card No Addon 1|PP Card No Addon 2|PP Card No Addon 3|Awb No.|Courier|Primary card Count|Addon Card Count|Total card Count|Bin|Logo|Gender Code|Varient'+'\n')
    scan_file.writelines(contents)       

df = pd.read_csv('AUF_CREDIT_SCANNING_CARD_FILE.csv',encoding= 'unicode_escape', sep='|', dtype=object)
df.to_excel('AUF_CREDIT_SCANNING_CARD_FILE'+'.xlsx', 'Sheet1', index=False)
os.remove('AUF_CREDIT_SCANNING_CARD_FILE.csv')
os.remove('xAUF_CREDIT_SCANNING_CARD_FILE.txt')