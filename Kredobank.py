#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import pandas as pd
import re

fname = "../26507010664701_980.txt"
fh = open(fname).read()
fh = fh.replace('\n','')
lst = re.split(r'-{80}', fh)
newlst = list()
for i in range(len(lst)):
    if not lst[i].startswith('Док.№'): continue
    no = lst[i][lst[i].find('Док.№')+5:lst[i].find('Док.№')+16].strip()
    date = lst[i][lst[i].find('Проведен')+8:lst[i].find('Проведен')+19].strip()
    nazv_platn = lst[i][lst[i].find('Платник   |')+27:lst[i].find('Платник   |')+59].strip()
    edr_platn = lst[i][lst[i].find('Платник   |')+66:lst[i].find('Платник   |')+80].strip()
    nazv_bank_platn = lst[i][lst[i].find('Банк плат |')+18:lst[i].find('Банк плат |')+79].strip()
    mfo_platn = lst[i][lst[i].find('Банк плат |')+11:lst[i].find('Банк плат |')+17].strip()
    acc_platn = lst[i][lst[i].find('Платник   |')+11:lst[i].find('Платник   |')+26].strip()
    uah = lst[i][lst[i].find('Сума')+4:lst[i].find('Сума')+21].strip()
    
    nazv_oderz = lst[i][lst[i].find('Отримувач |')+27:lst[i].find('Отримувач |')+59].strip()
    edr_oderz = lst[i][lst[i].find('Отримувач |')+66:lst[i].find('Отримувач |')+80].strip()
    nazv_bank_oderz = lst[i][lst[i].find('Банк отрим|')+18:lst[i].find('Банк отрим|')+79].strip()
    mfo_oderz = lst[i][lst[i].find('Банк отрим|')+11:lst[i].find('Банк отрим|')+17].strip()
    acc_oderz = lst[i][lst[i].find('Отримувач |')+11:lst[i].find('Отримувач |')+26].strip()
    prizn = lst[i][lst[i].find('Призн.плат|')+11:].strip()
    if acc_platn == '26507010664701':
        korresp = nazv_oderz; edrpou = edr_oderz; acc = acc_oderz; bank = nazv_bank_oderz; mfo = mfo_oderz; debit = re.sub(r'\s','', uah); kredit = 0;
    else:
        korresp = nazv_platn; edrpou = edr_platn; acc = acc_platn; bank = nazv_bank_platn; mfo = mfo_platn; debit = 0; kredit = re.sub(r'\s','', uah);
    prizn = ' '.join(prizn.split())#Удаляем лишние пробелы из назначения платежа
    prizn = re.sub(r'\|','', prizn)
    lst[i] = [date, no, korresp, edrpou, acc, bank, mfo, debit, kredit, prizn]#Пишем параметры платежа в список
    newlst.append(lst[i])
    #print(lst[i])
#print(lst)
df = pd.DataFrame(newlst, columns=['Дата', '№', 'Контрагент', 'ЄДРПОУ', 'Счет', 'Банк', 'МФО', 'Дебет', 'Кредит', 'Призначення'])
print(df)
df.to_excel('KredoSalam26507010664701.xlsx', sheet_name='26507010664701', index=False)
    
    
