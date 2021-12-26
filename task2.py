import sqlite3
import pandas as pd
import numpy
import matplotlib.pyplot as plt
import re

con = sqlite3.connect('works.sqlite')
df = pd.read_csv("works.csv")
cursor = con.cursor()
def clean(field):
    return re.sub(r'\<[^>]*\>', '', str(field))

df['skills'] = df['skills'].apply(clean)
df['otherInfo'] = df['otherInfo'].apply(clean)

df.to_sql("works", con, if_exists='append', index=False)
con.commit()

cursor.execute('drop table if exists genders')
cursor.execute('CREATE TABLE genders('
               'id INTEGER PRIMARY KEY AUTOINCREMENT,'
               'gender TEXT)')
cursor.execute('INSERT INTO genders(gender)'
               'SELECT DISTINCT gender'
               'FROM works WHERE gender IS NOT NULL')
cursor.execute('ALTER TABLE works'
               'ADD COLUMN gender_id INTEGER REFERENCES genders(id)')
cursor.execute('UPDATE works SET gender_id ='
               '(SELECT id FROM genders'
               'WHERE gender = works.gender)')
cursor.execute('ALTER TABLE works'
               'DROP COLUMN gender')
con.commit()

cursor.execute('drop table if exists education')
cursor.execute('CREATE TABLE education'
               '(id INTEGER PRIMARY KEY AUTOINCREMENT, '
               'level_of_edu TEXT)')
cursor.execute('INSERT INTO education(level_of_edu)'
               ' SELECT DISTINCT educationType '
               'FROM works'
               ' WHERE educationType IS NOT NULL')
cursor.execute('ALTER TABLE works'
               ' ADD COLUMN educationType_id INTEGER REFERENCES education(id)')
cursor.execute('UPDATE works'
               ' SET educationType_id ='
               ' (SELECT id'
               ' FROM education'
               ' WHERE level_of_edu = works.educationType)')
cursor.execute('ALTER TABLE works'
               ' DROP COLUMN educationType')
con.commit()