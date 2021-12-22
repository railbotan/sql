import sqlite3
import pandas as pd
import numpy
import matplotlib.pyplot as plt
# task1 and task2
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

#task 3, 4, 5, 6, 7
cursor.execute('SELECT COUNT(*) FROM works')
print(cursor.fetchall()[0][0])

cursor.execute('SELECT COUNT(*) FROM works WHERE gender = "Женский"')
w_salary = [t[0] for t in cursor.fetchall()]
cursor.execute('SELECT COUNT(*) FROM works WHERE gender = "Мужской"')
m_salary = [t[0] for t in cursor.fetchall()]
cursor.execute('SELECT gender, COUNT(*) FROM works GROUP BY gender')
cursor.execute('SELECT skills FROM works WHERE skills NOT NULL')
cursor.execute('SELECT salary FROM works WHERE skills LIKE "%Python%"')

#tasks 8, 9
percentiles = numpy.linspace(.1, 1, 10)

w_salary = numpy.quantile(w_salary, percentiles)
m_salary = numpy.quantile(m_salary, percentiles)

plt.hist(m_salary, bins=100)
plt.show()
plt.hist(w_salary, bins=100)
plt.show()

plt.plot(percentiles, m_salary)
plt.xlabel("Перцентили")
plt.ylabel("Зарплата у мужчин")
plt.show()

plt.plot(percentiles, w_salary)
plt.xlabel("Перцентили")
plt.ylabel("Зарплата у женщин")
plt.show()