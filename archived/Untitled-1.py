

def contains_special_characters(input_string):
            for char in input_string:
                asscii_value = ord(char)
                if 65 <= int(asscii_value) <= 90 or 97 <= int(asscii_value) <= 122 or int(asscii_value) == 32:
                    a = True
                else:
                    a = False
                    return a
                    # break
            return a


s = '$ANGAM*INDIA LIMITED                '
s= s.strip()
a = contains_special_characters(s)
print(a)