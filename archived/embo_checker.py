import re
# def embo_name_checker(embo_dataline):
#             a = embo_dataline
#             b = a[54:130]
#             if b.__contains__('.'):
#                 b= b.replace('.',' ')
#                 d = b
#                 d = d.ljust(76)
#                 f = a[:54]+d+a[130:]
#                 # print(d)
#                 f = a[:54]+d+a[130:]
#                 # print(d)
#                 return f
#             else:
#                 return a
def embo_name_checker(embo_dataline):
        a = embo_dataline
        b = a[55:130]
        # print(b)
        dummy_count = b.count(' . ')
        count = (b.count('. ') + b.count(' . ')+ b.count(' .'))-(dummy_count*2)
        c = b.replace('. ', ' ').replace(' . ', '  ').replace(' .', ' ')
        c1 = c.count('.')
        d = c.replace('.', '')
        count = count + c1
        if len(d) <= 76:
            d = d[:76-count] + ' ' * count + d[76-count:]
        f = a[:55]+d+a[130:]
        # line = f
        # print(f)
        return f
def embo_name_checker_1(embo_dataline):
        a = embo_dataline
        b = a[54:130]
        if b.__contains__('.'):
            # b= b.replace('.',' ')
            b = re.sub(r'\s+\.\s+', ' ', b)           # Replace dot surrounded by spaces with space
            b = re.sub(r'(?<=\w)\.(?=\w)', '', b)
            b = b.ljust(76)
            f = a[:54]+b+a[130:]
            # print(d)
            f = a[:54]+b+a[130:]
            # print(d)
            return f
        else:
            return a
def embo_name_checker_2(embo_dataline):
            a = embo_dataline
            b = a[54:130]
            if b.__contains__('.'):
                b= b.replace('.',' ')
                # d = " ".join(b.split())
                d = b
                d = d.ljust(76)
                f = a[:54]+d+a[130:]
                # print(d)
                f = a[:54]+d+a[130:]
                # print(d)
                return f
            else:
                return a
def embo_name_checker_3(embo_dataline):
            a = embo_dataline
            b = a[54:130]
            if b.__contains__('.'):
                b= b.replace('.',' ')
                d = " ".join(b.split())
                # d = b
                d = d.ljust(76)
                f = a[:54]+d+a[130:]
                # print(d)
                f = a[:54]+d+a[130:]
                # print(d)
                return f
            else:
                return a

def embo_name_checker_4(embo_dataline):
            a = embo_dataline
            b = a[54:130]
            y = b[:40]
            z = b[40:]
            if b.__contains__('.'):
                y= y.replace('.','')
                y = y.ljust(40)
                z= z.replace('.','')
                z = z.ljust(36)

                f = a[:54]+y+z+a[130:]
                return f
            else:
                return a

# print('1699110006530239112051412000100000C0001699116881279390ANKIT .                                 R.K STUDIO & LAB                    202')
# print(embo_name_checker('1699110006530239112051412000100000C0001699116881279390ANKIT .                                 R.K STUDIO & LAB                    202'))
# print(embo_name_checker('1699110006530239112051412000100000C0001699116881279390ANK.IT                                                                       202'))

data = '1699110006530239112051412000100000C0001699116881279390AN..KIT .      ..                   1254R.K STUDIO & LAB                    202'
print(data)
print(embo_name_checker(data))
# print(embo_name_checker_1(data))

# print(embo_name_checker_2(data))
# print(embo_name_checker_3(data))
print(embo_name_checker_4(data))


# import os
# import glob
# from pathlib import Path


# os.chdir(Path(r'A:\Sdrive\LIVE\AU_Credit\merger'))
       
# files = glob.glob('*.txtt')
# for file in files:
#     with open (file,'r') as data_in,  open ('data.txt','a') as data_out:
#         contents = data_in.readlines()
#         data_out.writelines(contents)
# fourth_line_logo_list = ['803','911','101','701','702','703','601','602','603']
# plastic_id = '0000000015' 
# logo_acc = '011'                    
# if plastic_id == '0000000015' and logo_acc not in fourth_line_logo_list:
#     retail_card_type = 'FIELD CLUB MEMBER'
#     print(retail_card_type)