# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 18:39:31 2022

@author: Administrator
"""

import pandas as pd

def pp_dup_check(number):
    with open('./config/BD_AWB - Copy.txt','r+') as file_read:
        contents = file_read.readlines()
        new_contents = [x[:-1] for x in contents]
        #contents = contents.replace("\n","")
        
        print(number)
        print(new_contents)
        #number = int(number)
        #number_check = number+"\n"
        if number in new_contents:
            print("number found")
            file_read.close()
            number = int(number)+1
            return(pp_dup_check(str(number)))
            
            
        else:
            print("not found")
            file_read.write(number)
            file_read.close()
            return number
    

print(pp_dup_check('12458459777')    )
