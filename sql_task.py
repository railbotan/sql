import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re


def delete_html(field):
    return re.sub(r'\<[^>]*\>', '', str(field))



con = sqlite3.connect('works.sqlite')
cursor = con.cursor()
cursor.execute('drop table if exists works')
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
con.commit()

df = pd.read_csv("works.csv")
df.to_sql("works", con, if_exists='append', index=False)
con.commit()

# Вторая часть ДЗ
df['skills'] = df['skills'].apply(delete_html)
df['otherInfo'] = df['otherInfo'].apply(delete_html)

#Работа на паре
cursor.execute('create index salary_index on works (salary)')
con.commit()
# Количество всех записей
cursor.execute('SELECT COUNT(*) FROM works')
print(cursor.fetchall()[0][0])
# Количество мужчин
cursor.execute('SELECT COUNT(*) FROM works where gender = "Мужской"')
print(cursor.fetchall()[0][0])
# Количество женщин
cursor.execute('SELECT COUNT(*) FROM works where gender = "Женский"')
print(cursor.fetchall()[0][0])
# У скольки записей заполены skills?
cursor.execute('SELECT COUNT(*) FROM works where skills not null')
print(cursor.fetchall()[0][0])
# Получить заполненные скиллы.
cursor.execute('SELECT skills FROM works where skills not null')
print(cursor.fetchall())
# Вывести зарплату только у тех, у кого в скилах есть Python
cursor.execute('SELECT salary FROM works where skills LIKE "%Python%"')
print(cursor.fetchall())
# Построить перцентили и разброс по з/п у мужчин и женщин.
# Мужчины
cursor.execute('SELECT salary FROM works where gender = "Мужской"')
men_salary = [t[0] for t in cursor.fetchall()]
print(men_salary)
# Женщины
cursor.execute('SELECT salary FROM works where gender = "Женский"')
women_salary = [t[0] for t in cursor.fetchall()]
print(women_salary)

# Графики
plt.plot()
men_salary = np.quantile(men_salary, np.linspace(0.1, 1, 10))
women_salary = np.quantile(women_salary, np.linspace(0.1, 1, 10))

plt.hist(men_salary, bins=100, color='blue')
plt.show()
plt.hist(women_salary, bins=100, color='blue')
plt.show()

# Создание таблицы по полю gender
cursor.execute('drop table if exists genders')
cursor.execute('create table genders(id INTEGER PRIMARY KEY AUTOINCREMENT, gender_val TEXT)')
con.commit()

cursor.execute('INSERT INTO genders(gender_val) SELECT DISTINCT gender FROM works WHERE gender IS NOT NULL')
con.commit()

cursor.execute('ALTER TABLE works ADD COLUMN gender_id INTEGER REFERENCES genders(id)')
con.commit()

cursor.execute('UPDATE works SET gender_id = (SELECT id FROM genders WHERE gender_val = works.gender)')
con.commit()

cursor.execute('ALTER TABLE works DROP COLUMN gender')
con.commit()

# Создание таблицы для образования
cursor.execute('drop table if exists education')
cursor.execute('create table education(id INTEGER PRIMARY KEY AUTOINCREMENT, edu_val TEXT)')
con.commit()

cursor.execute('INSERT INTO education(edu_val) SELECT DISTINCT educationType FROM works WHERE educationType IS NOT NULL')
con.commit()

cursor.execute('ALTER TABLE works ADD COLUMN educationType_id INTEGER REFERENCES education(id)')
con.commit()

cursor.execute('UPDATE works SET educationType_id = (SELECT id FROM education WHERE edu_val = works.educationType)')
con.commit()

cursor.execute('ALTER TABLE works DROP COLUMN educationType')
con.commit()





