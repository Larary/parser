#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import pandas as pd
import re
from dateutil import parser

fname = "../2650915269.txt"
fh = open(fname).read()
#fh = fh.replace('\n','')#Переводим весь файл в одну строку
fh = fh.replace('\xa0','')
clearstart = fh.find('Кредит')
clearfin = fh.find('Обороти за період:')
text = fh[clearstart+7:clearfin].strip()
text = re.sub(r'Дата проводки	\d{2}.\d{2}.\d{4}', '', text)
res = text.split('\n')
t = list()
lst=list()
for elem in res:
    if re.match('\t\d{2}.\d{2}.\d{4}\t\d.+', elem): 
        lst.append(t)
        t = [elem]
    else:        
        t.append(elem)
del lst[0]
print(len(lst))
for i in range(len(lst)):
    tstr = ''.join(lst[i])
    edrpou = re.search(r'ЄДРПОУ:[\s,\t](\d+)', tstr).group(1).strip()
    point2 = re.search(r'ЄДРПОУ:[\s,\t]\d+', tstr).end()
    point1 = re.search(r'ЄДРПОУ:[\s,\t]\d+', tstr).start()
    prizn = tstr[point2+1:].strip()
    prizn = ' '.join(prizn.split())#Удаляем лишние пробелы из назначения платежа
    acc = re.search(r'\t\t[\s,\t](\d+)', tstr).group(0).strip()
    point3 = re.search(r'\t\t[\s,\t](\d+)', tstr).end()
    korresp = tstr[point3+1:point1].strip()
    lst[i] = tstr.split('\t')
    date = lst[i][1]
    no = lst[i][3]
    debit = lst[i][4]
    kredit = lst[i][5]
    bank = lst[i][7]
    mfo = lst[i][6]
    lst[i] = [date, no, korresp, edrpou, acc, bank, mfo, debit, kredit, prizn]#Пишем параметры платежа в список
    
    
#print(lst)
df = pd.DataFrame(lst, columns=['Дата', '№', 'Контрагент', 'ЄДРПОУ', 'Счет', 'Банк', 'МФО', 'Дебет', 'Кредит', 'Призначення'])
print(df)
df.to_excel('2650915269.xlsx', sheet_name='2650915269', index=False)  