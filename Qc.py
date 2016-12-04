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

def get_average_gpa_best_worst_prof(cur):
    cur.execute("SELECT instructor, avg "\
                "FROM("\
                        "SELECT instructor, AVG(grade) "\
                        "FROM Meeting m, Student s "\
                        "WHERE m.cid = s.cid AND s.grade != 'nan' "\
                        "GROUP BY instructor"\
                    ") pag, "\
                    "("\
                        "SELECT MIN(avg), MAX(avg) "\
                        "FROM("\
                                "SELECT instructor, AVG(grade) "\
                                "FROM Meeting m, Student s "\
                                "WHERE m.cid = s.cid AND s.grade != 'nan' "\
                                "GROUP BY instructor"\
                            ") pag"\
                    ") mm "\
                "WHERE avg = min OR avg = max "\
                "GROUP BY avg, instructor;")
    return cur.fetchall()

def main():
    start_time = time.time()
    conn = connect()
    cur = conn.cursor()

    #PRINT HEADER
    print ("{0:<32} {1:<13}".format(
        "Instructor", "Average GPA"))

    # Get the percentage of students attempting n units for quarter
    results = get_average_gpa_best_worst_prof(cur)

    for i in range(0, len(results)):
        print ("{0:<12} {1:<13.2f}".format(
            results[i][0],
            results[i][1]))
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__': main()
