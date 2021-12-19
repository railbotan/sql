cursor.execute('SELECT gender, COUNT(*) FROM works group by gender')
print(cursor.fetchall())