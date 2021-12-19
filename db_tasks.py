import sqlite3
import pandas as pd
import re


def get_clean_field(field):
    return re.sub(r'\<[^>]*\>', '', str(field))


# создание базы данных и таблицы works
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
# ДЗ Скиллы и other info
# очистка поля skills от html тегов
df['skills'] = df['skills'].apply(get_clean_field)
# очистка поля otherInfo от html тегов
df['otherInfo'] = df['otherInfo'].apply(get_clean_field)

df.to_sql("works", con, if_exists='append', index=False)
con.commit()

# ДЗ
# Создание справочника по полю gender
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

# # содержание таблицы-справочника по гендерам
# cursor.execute('SELECT * FROM genders')
# print(cursor.fetchall())

# # вывод-проверка столбца гендер в таблице works
# cursor.execute('SELECT gender_val FROM genders,works WHERE genders.id = works.gender_id')
# print(cursor.fetchall())


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

# # содержание таблицы-справочника по образованию
# cursor.execute('SELECT * FROM education')
# print(cursor.fetchall())

# # вывод-проверка столбца образования в таблице works
# cursor.execute('SELECT edu_val FROM education,works WHERE education.id = works.educationType_id')
# print(cursor.fetchall())


# РАБОТА НА ПАРЕ
# cursor.execute('create index salary_index on works (salary)')
# con.commit()
# # количество всех записей
# cursor.execute('SELECT COUNT(*) FROM works')
# print(cursor.fetchall()[0][0])
# # men
# cursor.execute('SELECT COUNT(*) FROM works where gender = "Мужской"')
# print(cursor.fetchall()[0][0])
# # women
# cursor.execute('SELECT COUNT(*) FROM works where gender = "Женский"')
# print(cursor.fetchall()[0][0])
# # другой способ
# cursor.execute('SELECT gender, COUNT(*) FROM works group by gender')
# print(cursor.fetchall())
# # У скольки записей заполены skills?
# cursor.execute('SELECT COUNT(*) FROM works where skills not null')
# print(cursor.fetchall()[0][0])
# # # Получить заполненные скиллы.
# # cursor.execute('SELECT skills FROM works where skills not null')
# # print(cursor.fetchall())
# # Вывести зарплату только у тех, у кого в скилах есть Python
# cursor.execute('SELECT salary FROM works where skills LIKE "%Python%"')
# print(cursor.fetchall())
# Построить перцентили и разброс по з/п у мужчин и женщин.
# men
# cursor.execute('SELECT salary FROM works where gender = "Мужской"')
# m_salary = [t[0] for t in cursor.fetchall()]
# # print(m_salary)
#
# # women
# cursor.execute('SELECT salary FROM works where gender = "Женский"')
# w_salary = [t[0] for t in cursor.fetchall()]
# # print(w_salary)
#
# plt.plot()
# m_salary = np.quantile(m_salary, np.linspace(0.1, 1, 10))
# w_salary = np.quantile(w_salary, np.linspace(0.1, 1, 10))
#
# plt.hist(m_salary, bins=100, color='blue')
# plt.show()
# plt.hist(w_salary, bins=100, color='red')
# plt.show()
#
# # другой способ
# plt.plot(np.linspace(0.1, 1, 10), m_salary)
# plt.plot(np.linspace(0.1, 1, 10), w_salary)
# plt.xlabel("Перцентили")
# plt.ylabel("Зарплата")
#
# plt.show()