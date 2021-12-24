import math
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os.path

connection = sqlite3.connect("task.sqlite")
cursor = connection.cursor()

cursor.execute("drop table if exists works")

cursor.execute("create table works("
               "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
               "salary INTEGER,"
               "educationType TEXT,"
               "jobTitle TEXT,"
               "qualification TEXT,"
               "gender TEXT,"
               "dateModify TEXT,"
               "skills TEXT,"
               "otherInfo TEXT"
               ");")

connection.commit()

data = pd.read_csv('works.csv')
data.to_sql('works', connection, if_exists="append", index=None)
connection.commit()
cursor.execute("select * from works limit 5")
print(cursor.fetchall())
print(os.path.getsize("task.sqlite") / 1024 / 1024, "Mб")
cursor.execute("create index salary_index on works(salary);")
connection.commit()

cursor.execute("select count(*) from works")
cursor.execute("select count(*) from works where gender='Мужской'")
cursor.execute("select count(*) from works where gender='Женский'")
cursor.execute("select gender,count(*) from works group by gender")
print(cursor.fetchall())
cursor.execute('select count(*) from works where skills not null')
print(cursor.fetchall())
cursor.execute('select skills from works where skills not null')
print(cursor.fetchall())
cursor.execute("select salary from works where skills like '%Python%'")
print(cursor.fetchall())
print(os.path.getsize("task.sqlite") / 1024 / 1024, "Mб")
cursor.execute("select salary from works where gender = 'Мужской'")
mens_salary = [row[0] for row in cursor.fetchall()]
cursor.execute("select salary from works where gender = 'Женский'")
women_salary = [row[0] for row in cursor.fetchall()]

percintile = np.linspace(0.1, 1, 10)
q = np.quantile(mens_salary, percintile)
q1 = np.quantile(women_salary, percintile)
print(list(zip(percintile, q)))
print(list(zip(percintile, q1)))

plt.plot(percintile, q, color="b")
plt.plot(percintile, q1, color="r")
plt.xlabel("Перцентили")
plt.ylabel("Зарплата женщин")
plt.show()

params = [("Мужской", "Высшее"), ("Мужской", "Незаконченное высшее"), ("Мужской", "Среднее"),
          ("Мужской", "Среднее профессиональное"), ("Женский", "Высшее"), ("Женский", "Незаконченное высшее"),
          ("Женский", "Среднее"), ("Женский", "Среднее профессиональное")]

for p in params:
    sql_query = f"SELECT salary FROM works WHERE gender = '{p[0]}' and educationType = '{p[1]}'"
    salary = [row[0] for row in cursor.execute(sql_query).fetchall()]
    plt.hist(salary, bins=100)
    plt.title(f"Зарплата {p[0]} с образованием {p[1]}")
    plt.show()

l = pow(10, -10)

x = np.linspace(0.0 * l, 1 * l, 100)
y = []
fig, ax = plt.subplots()
for i in x:
    temp_x = i
    temp_y = 2.0 / l * math.pow(np.sin(3.0 * 3.1415 * i / l), 2)
    y.append(temp_y)

plt.plot(x, y, scalex=True, scaley=True)
plt.show()
