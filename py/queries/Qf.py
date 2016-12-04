'''
Created on Dec 3, 2016

@author: jphelps, Rochenko
'''

import sys
import psycopg2
import os
import time

def connect():
    # user = os.environ['USER']
    user = "postgres"
    try:
        conn = psycopg2.connect(dbname="postgres", user=user)
        return conn
    except:
        print "Failed to connect to the database"

def get_best_performing_major_on_ABC_courses(cur):
    cur.execute("SELECT major, avg "\
                "FROM ("\
                        "SELECT major, AVG(grade) "\
                        "FROM Course c, Student s "\
                        "WHERE c.subject = 'ABC' "\
                            "AND c.cid = s.cid "\
                        "GROUP BY major"\
                     ") cmp, "\
                     "("\
                        "SELECT MIN(avg) as mingpa, MAX(avg) as maxgpa "\
                        "FROM ("\
                                "SELECT major, AVG(grade) "\
                                "FROM Course c, Student s "\
                                "WHERE c.subject = 'ABC' "\
                                "AND c.cid = s.cid "\
                                "GROUP BY major"\
                             ") cmp "\
                     ") mm "\
                "WHERE avg = mingpa OR avg = maxgpa "\
                "GROUP BY avg, major;")
    return cur.fetchall()

def main():
    start_time = time.time()
    conn = connect()
    cur = conn.cursor()

    #PRINT HEADER
    print ("{0:<9} {1:<12}".format("Major", "Average GPA"))

    # Get each the major that performs best/worst on ABC courses
    results = get_best_performing_major_on_ABC_courses(cur)

    for i in range(0, len(results)):
        print ("{0:<9} {1:<12} ".format(results[i][0], results[i][1]))

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__': main()
