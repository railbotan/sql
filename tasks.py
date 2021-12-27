import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('works.csv')
con = sqlite3.connect('works.sqlite')
cr = con.cursor()

cr.execute('drop table if exists works')
cr.execute('create table if not exists works'
           '( ID integer primary key autoincrement'
           ', salary integer'
           ', educationType text'
           ', jobTitle text'
           ', qualification text'
           ', gender text'
           ', dateModify text'
           ', skills text'
           ', otherInfo text)')
con.commit()

# print(cr.execute('pragma table_info(works)').fetchall())
df.to_sql('works', con, if_exists='append', index=False)
print(cr.execute('select * from works limit 5').fetchall())

# 2 before 6 348 KB
cr.execute('create index salary_index on works (salary)')
# after 6 684 KB
# cr.execute('drop index if exists salary_index on works (salary)')

df.to_sql("works", con, if_exists='append', index=False)
con.commit()

# # 3
# cr.execute('create index salary_index on works (salary)')
# con.commit()
# cr.execute('select count(*) from works')
# print("Кол-во записей:", cr.fetchall()[0][0])
#
# # 4
# cr.execute("select count(*) from works where gender = 'Мужской'")
# print("Кол-во мужчин:", cr.fetchall()[0][0])
#
# cr.execute("elect count(*) from works where gender = 'Женский'")
# print("Кол-во женщин:", cr.fetchall()[0][0])
#
# # 5
# cr.execute("select count(*) from works where skills not null")
# print("Записей с заполненными skills:", cr.fetchall()[0][0])
#
# # 6
# cr.execute("select skills from works where skills not null")
# print("skills:", cr.fetchall())
#
# # 7
# cr.execute("select salary from works where skills like '%Python%'")
# print("Зарплата тех, у кого в скилах есть Python:", cr.fetchall())
#
# # 8
# cr.execute("select salary from works where gender = 'Мужской'")
# m_salary = [t[0] for t in cr.fetchall()]
#
# cr.execute("select salary from works where gender = 'Женский'")
# w_salary = [t[0] for t in cr.fetchall()]
#
# m_salary_quantile = np.quantile(m_salary, np.linspace(0.1, 1, 10))
# w_salary_quantile = np.quantile(w_salary, np.linspace(0.1, 1, 10))
#
# m_quantile = np.quantile(m_salary, np.linspace(0.1, 1, 10))
# w_quantile = np.quantile(w_salary, np.linspace(0.1, 1, 10))
# plt.hist(m_quantile, 100)
# plt.show()
# plt.hist(w_quantile, 100)
# plt.show()
# # 9
# plt.plot(np.linspace(0.1, 1, 10), m_salary_quantile)
# plt.xlabel("Перцентили")
# plt.ylabel("Зарплата мужчин")
# plt.show()
# plt.plot(np.linspace(0.1, 1, 10), w_salary_quantile)
# plt.xlabel("Перцентили")
# plt.ylabel("Зарплата женщин")
# plt.show()
