cursor.execute('SELECT COUNT(*) FROM works where skills not null')
print(cursor.fetchall()[0][0])

# Получить заполненные скиллы.
cursor.execute('SELECT skills FROM works where skills not null')
print(cursor.fetchall())

# Вывести зарплату только у тех, у кого в скилах есть Python
cursor.execute('SELECT salary FROM works where skills LIKE "%Python%"')
print(cursor.fetchall())