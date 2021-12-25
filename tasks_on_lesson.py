import sqlite3
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

con = sqlite3.connect('works.sqlite')
cursor = con.cursor()
cursor.execute('drop table if exists works')
# 1
cursor.execute(
    'create table if not exists works (ID INTEGER PRIMARY KEY AUTOINCREMENT,salary INTEGER,educationType TEXT,'
    'jobTitle TEXT,qualification TEXT,gender TEXT,dateModify TEXT,skills TEXT,otherInfo TEXT)')
con.commit()

df = pd.read_csv('works.csv')
df.to_sql('works', con, if_exists='append', index=False)
con.commit()

# 2 6.3 kb
cursor.execute('create index salary_index on works (salary)')
con.commit()
# 6.6 kb

# 3
cursor.execute('SELECT COUNT(*) FROM works')
# print(cursor.fetchall()[0][0])

# 4
cursor.execute("SELECT COUNT(*) FROM works WHERE gender = 'Мужской'")
# print(cursor.fetchall()[0][0])

cursor.execute("SELECT COUNT(*) FROM works WHERE gender = 'Женский'")
# print(cursor.fetchall()[0][0])

# 5
cursor.execute("SELECT COUNT(*) FROM works WHERE skills NOT NULL")
# print(cursor.fetchall()[0][0])

# 6
cursor.execute("SELECT skills FROM works WHERE skills NOT NULL")
# print(cursor.fetchall())

# 7
cursor.execute("SELECT salary FROM works WHERE skills LIKE '%Python%'")
# print(cursor.fetchall())

# 8
cursor.execute("SELECT salary FROM works WHERE gender = 'Мужской'")
m_salary = [t[0] for t in cursor.fetchall()]
# print(m_salary)

cursor.execute("SELECT salary FROM works WHERE gender = 'Женский'")
w_salary = [t[0] for t in cursor.fetchall()]
# print(w_salary)

# 9
m_salary = np.quantile(m_salary, np.linspace(0.1, 1, 10))
w_salary = np.quantile(w_salary, np.linspace(0.1, 1, 10))

plt.hist(m_salary, bins=100, color='blue')
plt.show()
plt.hist(w_salary, bins=100, color='red')
plt.show()
