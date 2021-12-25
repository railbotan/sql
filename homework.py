import sqlite3
import pandas as pd
import re


def get_out_tags(field):
    return re.sub(r'\<[^>]*\>', '', str(field))


con = sqlite3.connect('works.sqlite')
cursor = con.cursor()
cursor.execute('drop table if exists works')
cursor.execute(
    'create table if not exists works (ID INTEGER PRIMARY KEY AUTOINCREMENT,salary INTEGER,educationType TEXT,'
    'jobTitle TEXT,qualification TEXT,gender TEXT,dateModify TEXT,skills TEXT,otherInfo TEXT)')
con.commit()

# Скиллы и otherInfo
df = pd.read_csv('works.csv')
df['skills'] = df['skills'].apply(get_out_tags)
df['otherInfo'] = df['otherInfo'].apply(get_out_tags)
df.to_sql('works', con, if_exists='append', index=False)
con.commit()

# ДЗ Пробуем нормализовать базу данных и немного почистить поля.
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

# Проверка вывода
# cursor.execute('SELECT * FROM genders')
# print(cursor.fetchall())
# cursor.execute('SELECT gender_val FROM genders,works WHERE genders.id = works.gender_id')
# print(cursor.fetchall())


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

# Проверка вывода
# cursor.execute('SELECT * FROM education')
# print(cursor.fetchall())
# cursor.execute('SELECT edu_val FROM education,works WHERE education.id = works.educationType_id')
# print(cursor.fetchall())

