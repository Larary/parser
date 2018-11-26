#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import pandas as pd
import re

fname = "../Privat26508052600049.txt"
fh = open(fname).read()
clearstart = fh.find('М Е М О Р I А Л Ь Н И Й О Р Д Е Р')
text = fh[clearstart:].strip()
text = text.replace('\x0c\n','')
lst = re.split(r'Час пров.', text)
lst.pop()
for i in range(len(lst)):
    tstr = ''.join(lst[i])
    no = tstr[tstr.find('| N:')+4:tstr.find('|tr.')].strip()
    date = tstr[tstr.find('вiд :')+5:tstr.find('г. ---')].strip()
    platnik = re.search(r'Платник (?:([\w,\s,\",(,),\.]+|\w+-[\w,\s,\"\.]+))-+[\s,\n]+Код\|\s(\d+)', tstr)
    #platnik = re.search(r'Платник (?:([\w,\s,\",(,),\.]+|Днiпр-ськаОДАТ"Райф.Б.Аваль[\s,\n]+))-+[\s,\n]+Код\|\s\d+', tstr).group(1)
    nazv_platn = platnik.group(1).strip()
    edr_platn = platnik.group(2)
    bank_platn = re.search(r'Банк платника -+([\w,\s,\",(,),\.,-]+)в м.___________________\| (\d{6}) \|\| (\d+)', tstr)
    nazv_bank_platn = bank_platn.group(1).strip()
    mfo_platn = bank_platn.group(2)
    acc_platn = bank_platn.group(3)
    uah = re.search(r'UAH (\d+\.\d{2})', tstr).group(1)
    #oderz = re.search(r'Одержувач ([\w,\s,\",\',(,),\.,-]+)[\s,\n,\|,-]+Код\|\s(\d+)', tstr)
    oderz = re.search(r'Одержувач ([\w,\s,\",\',(,),\.,\-,\+]+)[\w,\s,\n,\.,\|,-]+Код\|\s(\d+)', tstr)
    nazv_oderz = oderz.group(1)
    edr_oderz = oderz.group(2)
    bank_oderz = re.search(r'Банк одержувача -+\| \| \n([\w,\s,\",(,),\.,-]+) в м.___________________\| (\d{6}) \|\| (\d+)', tstr)
    nazv_bank_oderz = bank_oderz.group(1).strip()
    mfo_oderz = bank_oderz.group(2)
    acc_oderz = bank_oderz.group(3)
    prizn = re.search(r'Призначення платежу ([\w,\s,\",(,),\,,\.,\/,\',№,#,-]+)[\s,\|,-]+', tstr).group(1).strip()
    if acc_platn == '26508052600049':
        korresp = nazv_oderz; edrpou = edr_oderz; acc = acc_oderz; bank = nazv_bank_oderz; mfo = mfo_oderz; debit = uah; kredit = 0;
    else:
        korresp = nazv_platn; edrpou = edr_platn; acc = acc_platn; bank = nazv_bank_platn; mfo = mfo_platn; debit = 0; kredit = uah;
    
    lst[i] = [date, no, korresp, edrpou, acc, bank, mfo, debit, kredit, prizn]#Пишем параметры платежа в список
    #print(lst[i])

df = pd.DataFrame(lst, columns=['Дата', '№', 'Контрагент', 'ЄДРПОУ', 'Счет', 'Банк', 'МФО', 'Дебет', 'Кредит', 'Призначення'])
print(df)
df.to_excel('Privat26508052600049.xlsx', sheet_name='26508052600049', index=False)