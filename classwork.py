import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


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

cursor.execute('create index salary_index on works (salary)')
con.commit()
cursor.execute('SELECT COUNT(*) FROM works')
print(cursor.fetchall()[0][0])

cursor.execute("SELECT COUNT(*) FROM works WHERE gender = 'Мужской'")
print(cursor.fetchall()[0][0])

cursor.execute("SELECT COUNT(*) FROM works WHERE gender = 'Женский'")
print(cursor.fetchall()[0][0])

cursor.execute("SELECT gender, COUNT(*) FROM works group by gender")
print(cursor.fetchall())

cursor.execute("SELECT COUNT(*) FROM works WHERE skills NOT NULL")
print(cursor.fetchall()[0][0])

cursor.execute("SELECT skills FROM works WHERE skills NOT NULL")
print(cursor.fetchall())

cursor.execute("SELECT salary FROM works WHERE skills LIKE '%Python%'")
print(cursor.fetchall())


cursor.execute("SELECT salary FROM works WHERE gender = 'Мужской'")
m_salary = [t[0] for t in cursor.fetchall()]
# print(m_salary)

cursor.execute("SELECT salary FROM works WHERE gender = 'Женский'")
w_salary = [t[0] for t in cursor.fetchall()]
# print(w_salary)


m_salary = np.quantile(m_salary, np.linspace(0.1, 1, 10))
w_salary = np.quantile(w_salary, np.linspace(0.1, 1, 10))

plt.plot(np.linspace(0.1, 1, 10), m_salary)
plt.plot(np.linspace(0.1, 1, 10), w_salary)
plt.xlabel("Перцентили")
plt.ylabel("Зарплата")
plt.show()
