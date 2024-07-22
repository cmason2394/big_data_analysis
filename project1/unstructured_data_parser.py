# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 11:02:48 2024

@author: cassi
"""

import re
import numpy as np

text = '''
Center/Daycare
825 23rd Street South
Arlington, VA 22202
703-979-BABY (2229)
22.
Maria Teresa Desaba, Owner/Director; Tony Saba, Org. Director.
Web site: www.mariateresasbabies.com
Serving children 6 wks to 5yrs full-time.

National Science Foundation Child Development Center
23.
4201 Wilson Blvd., Suite 180 22203
703-292-4794
Web site: www.brighthorizons.com 112 children, ages 6 wks–5 yrs.
7:00 a.m. – 6:00 p.m. Summer Camp for children 5–9 years.
'''

print(text)

phoneNums = re.findall(r'^\d{3}-\d{3}-', text) #r'\d{3}-\d{4}-\d{4}' or r'\d{3}-\d{4}-\D{4}'

#print(phoneNums)

# function to pull out phone numbers
def findPhoneNums(string):
    if re.search(r'\d{3}-\d{3}-', string):
        return string
    else:
        return ''

# function to pull out addresses
def findAddress(string1, string2):
    if re.search('street|boulevard|st|blvd|avenue|ave|court|lane', string1):
        if re.search(r'\d{5}$', string1) is not True:
            if re.search(r'\d{5}$', string2):
                string = string1 + ' ' + string2
                return string
            else: 
                return string1
    else:
        return ''

# function to pull out website
def findWebSite(string):
    if re.search('www.|web site|.com', string):
        return string
    else:
        return ''

#function to pull out number/index
def findNumber(string):
    if re.fullmatch('\d{1,3}.', string):
        return string
    else:
        return ''

# function to pull operating hours
def findHours(string):
    if re.search('a.m|p.m.', string):
        return string
    else:
        return ''
    
# function to pull daycare name
def findName(string):
    if re.search('center|daycare', string):
        return string
    else:
        return ''

# function to split lines with too much info one one line
def splitInfo(lines):
    tempList = []
    for line in lines:
        #print(line)
        l = re.split('.com ', line) #re.split('.com  ', re.sub('.com', '.com.com', line))
        #print(l)
        #print(type(l))
        tempList.append(l)
    flatList = list(np.concatenate(tempList))
    return flatList

# clean data     
rawLines = text.splitlines()
#print(rawLines)

noEmptyLines = [i for i in rawLines if i]
    
lines = splitInfo(noEmptyLines)
#print(lines)
#print(type(lines))

# initialize lists
daycareCenters = []

# categorize each line
i=0
for line in lines:
    line = lines[i].lower()
    if i + 1 < len(lines):
        nextline = lines[i+1].lower()
    #print(i)
    #print(line)
    #print(nextline)
    if re.search(r'\d{3}-\d{3}-', line):
        phone = line
        daycareCenters.append({
            'phone': phone})
    elif re.search('street|boulevard|st|blvd|avenue|ave|court|lane', line):
        address = findAddress(line, nextline)
        daycareCenters.append({'address': address})
    elif re.search('www.|web site|.com', line):
        website = line
        daycareCenters.append({'website': website})
    elif re.fullmatch('\d{1,3}.', line):
        number = line
        daycareCenters.append({'number': number})
    elif re.search('a.m|p.m.', line):
        hours = line
        daycareCenters.append({'hours': hours})
    elif re.search('center|daycare', line):
        name = line
        daycareCenters.append({'name': name})
    else:
        description = line
        daycareCenters.append({'description': description})
    i+=1
    

print(daycareCenters)


    