#!/usr/bin/env 
'''
@Author Erik Grootendorst
@Title Project: Log Analysis
@Date 08-14-2019
@Class Full Stack Web Developer Nano Degree
@Description See README.md
'''
# Honestly I'm still very green at both python and SQL and would love
# any feedback on coding styles or tricks to use so as to increase readability
# and efficiency

import psycopg2
import sys


DBNAME = "news"
QUERY1 = '''select * from views limit 3'''

QUERY2 = '''select name, sum(count) as views
            from authors
            join (
                select author, works.title, count
                from works
                join views on works.title = views.title
                ) as a
            on authors.id = a.author
            group by name
            order by views desc'''

QUERY3 = '''select date, perror
            from errorStats
            where perror > 1.0'''


# I initialized the db object globally under the belief it is best practice
# as opposed to instantiating it in each method.
# Any feedback on this matter would be appreciated, I dont know if I could pass
# this object from the main method to better control it, as well as the cursor.

try:
    db = psycopg2.connect(database=DBNAME)
except psycopg2.Error as e:
    print ("Unable to connect to " + DBNAME)
    print (e.pgerror)
    print (e.diag.message_detail)
    sys.exit(1)
else:
    print ("Connected!")


def main():

    getPopArticles()
    getPopAuthors()
    getErrorLog()
    db.close()


# answer to question 1
def getPopArticles():

    # initialize cursor
    c = db.cursor()
    c.execute(QUERY1)

    # fetch results of query
    popArts = c.fetchall()

    print('\n*********************************************************')
    print('* What are the most popular three articles of all time? *')
    print('*********************************************************\n')

    for rows in popArts:
        # Line was too long according to PEP8, had to go to next line
        print('"{article}" - {count} views'
              .format(article=rows[0], count=rows[1]))

    print('')


# answer to question 2
def getPopAuthors():

    c = db.cursor()
    c.execute(QUERY2)

    popAuths = c.fetchall()

    print('\n*********************************************************')
    print('* Who are the most popular article authors of all time? *')
    print('*********************************************************\n')

    for rows in popAuths:
        print('"{author}" -  {count} views'
              .format(author=rows[0], count=rows[1]))

    print('')


# answer to question 3
def getErrorLog():

    c = db.cursor()
    c.execute(QUERY3)

    errorDays = c.fetchall()

    print('\n**************************************************************')
    print('* On which days did more than 1% of requests lead to errors? *')
    print('**************************************************************\n')

    for rows in errorDays:
        print('{date} - {:1.1f}% errors'.format(rows[1], date=rows[0]))

    print('')


if __name__ == "__main__":
    main()
