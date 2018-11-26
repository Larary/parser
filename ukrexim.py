# This Python file uses the following encoding: utf-8
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import pandas as pd
import re
from dateutil import parser

fname = "../p1.txt"
fh = open(fname).read()
fh = fh.replace('\n','')#Переводим весь файл в одну строку
dpos = fh.find('03/01/03')#Ищем первую запись выписки и удаляем все до нее, ищем последние строки и удаляем
epos = fh.find('Всього')
text = fh[dpos:epos].strip()

list =[]#Создаем пустой список

#Пока есть текст, отрезаем от него части с отдельными платежами
while len(text) > 0:
    endd = re.search(r'\d\d/\d\d/\d{2}', text).end()#Ищем номер последней цифры первой даты текста
    rest = text[endd+1:].strip()#Отрезаем текст после даты и сохраняем его
    if re.search(r'\d\d/\d\d/\d{2}', rest) is not None:#Ищем следующую дату, если она есть (если это не последняя запись)
        begnext = re.search(r'\d\d/\d\d/\d{2}', rest).start()#Находим номер первой цифры следующей даты
        #Записываем в искомую строку часть текста, начиная с первой даты
        #Прибавляем 9, т.к. искали begnext не с начала строки, а без первой даты
        line = text[:begnext+9].strip()
        text = rest[begnext:].strip()#Переписываем в переменную остаток текста
    #Если запись последняя, больше дат нет, записываем в строку остаток текста и обнуляем переменную текста
    else:
        line = text
        text = ''
    #Полученную строку делим на части
    date = parser.parse(line[:8], dayfirst=True).strftime('%d.%m.%Y')
    mfo = line[9:15]
    acc = line[16:32].rstrip()
    no = line[33:44].lstrip()
    edr = line.find('Код кор.:')
    bk = line.find('Банк кор.:')
    kor = line.find('Кор.:')
    edrpou = line[edr+10:bk].rstrip()
    bank = line[bk+10:kor].rstrip()
    korresp = line[kor+5:].rstrip()
    if re.search(r'\d+', line[45:82]) is not None:#Если не последний платеж
        debit = line[45:82].strip().replace(',','.')
        debit = float(re.sub(r'`','', debit))
        kredit = ''
        prizn = line[83:edr].strip()
    else:#Если последний платеж
        debit = ''
        kredit = line[45:121].strip().replace(',','.')
        kredit = float(re.sub(r'`','', kredit))
        prizn = line[122:edr].strip()
    
    prizn = ' '.join(prizn.split())#Удаляем лишние пробелы из назначения платежа
    
    t = [date, no, korresp, edrpou, acc, bank, mfo, debit, kredit, prizn]#Пишем параметры платежа в список
    list.append(t)#Пишем все списки платежей в большой список
     
df = pd.DataFrame(list, columns=['Дата', '№', 'Контрагент', 'ЄДРПОУ', 'Счет', 'Банк', 'МФО', 'Дебет', 'Кредит', 'Призначення'])
print(df)
df.to_excel('test.xlsx', sheet_name='sheet1', index=False)