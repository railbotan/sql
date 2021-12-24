import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 6 500 352
# 6 844 416
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

# 3
cursor.execute('create index salary_index on works (salary)')
con.commit()
cursor.execute('SELECT COUNT(*) FROM works')
print("Количество записей:", cursor.fetchall()[0][0])

# 4
cursor.execute("SELECT COUNT(*) FROM works WHERE gender = 'Мужской'")
print("Количество мужчин:", cursor.fetchall()[0][0])

cursor.execute("SELECT COUNT(*) FROM works WHERE gender = 'Женский'")
print("Количество женщин:", cursor.fetchall()[0][0])

# 5
cursor.execute("SELECT COUNT(*) FROM works WHERE skills NOT NULL")
print("Записей с заполенными skills:", cursor.fetchall()[0][0])

# 6
# cursor.execute("SELECT skills FROM works WHERE skills NOT NULL")
# print("skills:", cursor.fetchall())

# 7
cursor.execute("SELECT salary FROM works WHERE skills LIKE '%Python%'")
print("Зарплата тех, у кого в скилах есть Python:", cursor.fetchall())

# 8, 9
cursor.execute("SELECT salary FROM works WHERE gender = 'Мужской'")
m_salary = [t[0] for t in cursor.fetchall()]

cursor.execute("SELECT salary FROM works WHERE gender = 'Женский'")
w_salary = [t[0] for t in cursor.fetchall()]

m_salary_quantile = np.quantile(m_salary, np.linspace(0.1, 1, 10))
w_salary_quantile = np.quantile(w_salary, np.linspace(0.1, 1, 10))

plt.plot(np.linspace(0.1, 1, 10), m_salary_quantile)
plt.xlabel("Перцентили")
plt.ylabel("Зарплата мжучин")
plt.show()
plt.plot(np.linspace(0.1, 1, 10), w_salary_quantile)
plt.xlabel("Перцентили")
plt.ylabel("Зарплата женщин")
plt.show()
