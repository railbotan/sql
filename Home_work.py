import sqlite3
import pandas as pd
import re


def strip_tags(value):
    return re.sub(r'<[^>]*>', '', str(value))


con = sqlite3.connect('works.sqlite')
cursor = con.cursor()
cursor.execute('DROP TABLE IF EXISTS works')
cursor.execute('CREATE TABLE works ('
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
df['skills'] = df['skills'].apply(strip_tags)
df['otherInfo'] = df['otherInfo'].apply(strip_tags)
df.to_sql("works", con, if_exists='append', index=False)
con.commit()

cursor.execute('DROP TABLE IF EXISTS genders')
cursor.execute('CREATE TABLE genders(genderName TEXT PRIMARY KEY )')
cursor.execute('INSERT INTO genders SELECT DISTINCT gender FROM works WHERE gender IS NOT NULL')
cursor.execute('DROP TABLE IF EXISTS educations')
cursor.execute('CREATE TABLE educations(educationType TEXT PRIMARY KEY )')
cursor.execute('INSERT INTO educations SELECT DISTINCT educationType FROM works WHERE works.educationType IS NOT NULL')
con.commit()


cursor.execute('CREATE TABLE new_works ('
               'ID INTEGER PRIMARY KEY AUTOINCREMENT,'
               'salary INTEGER,'
               'educationType TEXT REFERENCES educations(educationType) ON DELETE CASCADE ON UPDATE CASCADE,'
               'jobTitle TEXT,'
               'qualification TEXT,'
               'gender TEXT REFERENCES genders(genderName) ON DELETE CASCADE ON UPDATE CASCADE,'
               'dateModify TEXT,'
               'skills TEXT,'
               'otherInfo TEXT)')
cursor.execute('INSERT INTO new_works SELECT * FROM works')
cursor.execute('DROP TABLE works')
cursor.execute('ALTER TABLE new_works RENAME TO works')
con.commit()
