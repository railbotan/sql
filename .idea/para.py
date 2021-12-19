cursor.execute('create index salary_index on works (salary)')
con.commit()

# количество всех записей
ursor.execute('SELECT COUNT(*) FROM works')
print(cursor.fetchall()[0][0])

# men
cursor.execute('SELECT COUNT(*) FROM works where gender = "Мужской"')
print(cursor.fetchall()[0][0])

# women
cursor.execute('SELECT COUNT(*) FROM works where gender = "Женский"')
print(cursor.fetchall()[0][0])