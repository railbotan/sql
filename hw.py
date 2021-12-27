import sqlite3
import pandas as pd
import re


def remove_tags(field):
    return re.sub(r'<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});', '', str(field))


con = sqlite3.connect('works.sqlite')
df = pd.read_csv("works.csv")
cr = con.cursor()

df['skills'] = df['skills'].apply(remove_tags)
df['otherInfo'] = df['otherInfo'].apply(remove_tags)

df.to_sql("works", con, if_exists='replace', index=False)
con.commit()

cr.execute('drop table if exists genders')
cr.execute('create table genders'
           '(genderName text primary key)')
cr.execute('insert into genders select distinct gender '
           'from works where gender is not null')

cr.execute('drop table if exists educations')
cr.execute('create table educations'
           '(educationType text primary key)')
cr.execute('insert into educations select distinct educationType '
           'from works where works.educationType is not null')
con.commit()

cr.execute('create table new_works '
           '( ID integer primary key autoincrement'
           ', salary integer'
           ', educationType text '
           'references educations(educationType) '
           'on delete cascade on update cascade'
           ', jobTitle text'
           ', qualification text'
           ', gender text '
           'references genders(genderName) '
           'on delete cascade on update cascade'
           ', dateModify text'
           ', skills text'
           ', otherInfo text)')
cr.execute('insert into new_works select * from works')
cr.execute('drop table works')
cr.execute('alter table new_works rename to works')
con.commit()
