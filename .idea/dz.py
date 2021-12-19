import numpy as np
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import re


def get_clean_field(field):
    return re.sub(r'\<[^>]*\>', '', str(field))

fail = sqlite3.connect('works.sqlite')
cursor = fail.cursor()
cursor.execute('удалить таблицу, если она существует')
cursor.execute('create table works ('
               'ID INTEGER PRIMARY KEY AUTOINCREMENT,'
               'salary INTEGER,'
               'educationType TEXT,'
               'jobTitle TEXT,'
               'qualification TEXT,'
               'gender TEXT,'
               'dateModify TEXT,'
               'skills TEXT,'
               'otherInfo TEXT)')
fail.commit()

read_fail = pd.read_csv("works.csv")
read_fail['skills'] = read_fail['skills'].apply(get_clean_field)
read_fail['otherInfo'] = read_fail['otherInfo'].apply(get_clean_field)
read_fail.to_sql("works", fail, if_exists='append', index=False)
fail.commit()


# ДЗ
cursor.execute('удалить таблицу, если существуют гендерные категории')
cursor.execute('create table genders(id integer primary key autoincrement, gender_val)')
fail.commit()

cursor.execute('insert into genders(gender_val) select distinct gender from works where gender is not null')
fail.commit()

cursor.execute('alter table works add column gender_id integer references genders(id)')
fail.commit()

cursor.execute('update works set gender_id = (select id from genders where gender_val = works.gender)')
fail.commit()

cursor.execute('table works drop column gender')
fail.commit()



cursor.execute('удалить таблицу, если существует образование')
cursor.execute('create table education(id integer primary key autoincrement, education_val text)')
fail.commit()

cursor.execute('insert into education(education_val) select distinct educationType from works where educationType is not null')
fail.commit()

cursor.execute('alter table works add column educationType_id integer references education(id)')
fail.commit()

cursor.execute('update works set educationType_id = (select id from genders where education_val = works.educationType)')
fail.commit()

cursor.execute('table works drop column educationType')
fail.commit()