import pandas as pd
import os
import glob
from datetime import datetime, date

import pandas as pd

def Excel_to_csv(file):
    df = pd.read_excel(file, dtype=object)
    df.to_csv(file[:-5] + '.csv', index=False, sep='|', encoding='utf-8')
    

# def Excel(file):
    # df = pd.read_csv(file,encoding= 'unicode_escape', sep='|', dtype=object)
    # df.to_excel(file[:-4]+'_UPDATED_FILE'+'.xlsx', 'Sheet1', index=False)

def get_Ncb_wel(afcid,card_type):
    wel,ncb = 'N/A','N/A'
    card_type = card_type.upper()
    if card_type.__contains__('NEW'):
        input_files = glob.glob('*PACKING_LIST*.csv') 
        for f in input_files:
            with open(f,'r') as infile_dis:
                contents = infile_dis.readlines()
                for line in contents:
                    val = line.split('|')
                    id = val[-9].strip()
                    if afcid == id:
                        wel = val[-10].strip()
                        ncb = wel.replace('WEL','NCB')
                        return wel,ncb
                
    return wel,ncb


input_files = glob.glob('*NCB*.xlsx') + glob.glob('*PACKING_LIST*.xlsx')
for f in input_files:
    Excel_to_csv(f)


input_files = glob.glob('*NCB*.csv')
for f in input_files:
    with open(f, 'r') as infile, open(f[:-4] + '.txt', 'a') as outfile:
        lines = infile.readlines()
        outfile.write(lines[0])
        for line in lines[1:]:
            parts = line.strip().split('|')
            afcid = parts[3].strip()
            card_type = parts[-5].strip()
            WEL, NCB = get_Ncb_wel(afcid, card_type)
            parts[4], parts[5] = NCB, WEL  # Replace NCB and WEL
            outfile.write('|'.join(parts) + '\n')

for fi in glob.glob('*.txt'):
    df = pd.read_csv(fi,encoding= 'unicode_escape', sep='|', dtype=object)
    df.to_excel(fi[:-4]+'_UPDATED_FILE'+'.xlsx', 'Sheet1', index=False)

print("Closing...") 
input('Please ENTER any Button')