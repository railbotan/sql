import re
import sqlite3
import pandas as pd


def createTables():
    cursor.execute("drop table if exists works")
    cursor.execute("drop table if exists gender")
    cursor.execute("drop table if exists education")
    cursor.execute("create table gender("
                   "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "gender TEXT"
                   ");")
    cursor.execute("create table education("
                   "id INTEGER primary key autoincrement,"
                   "educationType TEXT"
                   ");")
    cursor.execute("create unique index education_educationType_uindex on education (educationType);")
    cursor.execute("create unique index gender_gender_uindex on gender (gender);")
    cursor.execute("create table works("
                   "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "salary INTEGER,"
                   "educationType references education,"
                   "jobTitle TEXT,"
                   "qualification TEXT,"
                   "gender references gender,"
                   "dateModify TEXT,"
                   "skills TEXT,"
                   "otherInfo TEXT"
                   ");")

    connection.commit()


def clearFromHtml(line):
    if not isinstance(line, str):
        return line
    clean = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    a = re.sub(clean, '', line)
    return a


connection = sqlite3.connect("homework.sqlite")
cursor = connection.cursor()
createTables()

data = pd.read_csv('works.csv')

for i in data['gender'].drop_duplicates():
    cursor.execute(f"insert into gender(gender) values('{i}');")

for i in data['educationType'].drop_duplicates():
    cursor.execute(f"insert into education (educationType) values ('{i}');")

connection.commit()

index = 1
for key, values in data.iterrows():
    cursor.execute(f"select id from education where educationType='{values['educationType']}';")
    education_id = cursor.fetchone()[0]

    cursor.execute(f"select id from gender where gender='{values['gender']}';")
    gender_id = cursor.fetchone()[0]

    cursor.execute("insert into works "
                   "(salary, educationType, jobTitle, qualification, gender, dateModify, skills, otherInfo)"
                   f"values ("
                   f"'{values['salary']}',"
                   f"'{education_id}',"
                   f"'{values['jobTitle']}',"
                   f"'{values['qualification']}',"
                   f"'{gender_id}',"
                   f"'{values['dateModify']}',"
                   f"'{clearFromHtml(values['skills'])}',"
                   f"'{clearFromHtml(values['otherInfo'])}');")
    connection.commit()
    print(f"Добавленна {index} строка")
    index += 1

connection.commit()
