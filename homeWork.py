import pandas as pd
import sqlite3 as sql
import re
def clean(file):
    return re.sub(r'\<[^>]*\>', '', str(file))
connection = sql.connect('homeworks.sqlite')
cursor = connection.cursor()
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
connection.commit()
df = pd.read_csv('works.csv')
df.to_sql("works", connection, if_exists='append', index=False)

df['skills'] = df['skills'].apply(clean)
df['otherInfo'] = df['otherInfo'].apply(clean)
connection.commit()

cursor.execute('drop table if exists genders')
cursor.execute('create table genders(id INTEGER PRIMARY KEY AUTOINCREMENT, gender_val TEXT)')
connection.commit()

cursor.execute('INSERT INTO genders(gender_val) SELECT DISTINCT gender FROM works WHERE gender IS NOT NULL')
connection.commit()

cursor.execute('ALTER TABLE works ADD COLUMN gender_id INTEGER REFERENCES genders(id)')
connection.commit()

cursor.execute('UPDATE works SET gender_id = (SELECT id FROM genders WHERE gender_val = works.gender)')
connection.commit()

cursor.execute('ALTER TABLE works DROP COLUMN gender')
connection.commit()

cursor.execute('drop table if exists education')
cursor.execute('create table education(id INTEGER PRIMARY KEY AUTOINCREMENT, edu_val TEXT)')
connection.commit()

cursor.execute('INSERT INTO education(edu_val) SELECT DISTINCT educationType FROM works WHERE educationType IS NOT NULL')
connection.commit()

cursor.execute('ALTER TABLE works ADD COLUMN educationType_id INTEGER REFERENCES education(id)')
connection.commit()

cursor.execute('UPDATE works SET educationType_id = (SELECT id FROM education WHERE edu_val = works.educationType)')
connection.commit()

cursor.execute('ALTER TABLE works DROP COLUMN educationType')
connection.commit()