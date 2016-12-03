'''
Created on Dec 3, 2016

@author: jphelps, Rochenko
'''

import sys
import psycopg2
import os
import time

def connect():
    user = os.environ['USER']
    # user = "postgres"
    try:
        conn = psycopg2.connect(dbname="postgres", user=user)
        return conn
    except:
        print "Failed to connect to the database"

def get_average_gpa_best_worst_prof_abc(cur):
    cur.execute("SELECT cpg.crse, instructor, avg "\
                "FROM ("\
                        "SELECT crse, instructor, AVG(grade) "\
                        "FROM Course c, Meeting m, Student s "\
                        "WHERE c.subject = 'ABC' AND crse>99 "\
                            "AND crse<200 AND c.cid=m.cid "\
                            "AND m.cid=s.cid "\
                        "GROUP BY crse, instructor"\
                     ") cpg, "\
                     "("\
                        "SELECT crse, MIN(avg), MAX(avg) "\
                        "FROM ("\
                                "SELECT crse, instructor, AVG(grade) "\
                                "FROM Course c, Meeting m, Student s "\
                                "WHERE c.subject = 'ABC' AND crse>99 "\
                                    "AND crse<200 AND c.cid=m.cid "\
                                    "AND m.cid=s.cid "\
                                "GROUP BY crse, instructor"\
                             ") cpg "\
                        "GROUP BY crse"\
                     ") mm "\
                "WHERE cpg.crse = mm.crse AND (avg=min OR avg=max) "\
                "ORDER BY cpg.crse, avg;")
    return cur.fetchall()

def main():
    start_time = time.time()
    conn = connect()
    cur = conn.cursor()

    #PRINT HEADER
    print ("{0:<9} {1:<9}                       {2:<9}".format(
        "Course", "Instructor", "Average GPA"))

    # Get the percentage of students attempting n units for quarter
    results = get_average_gpa_best_worst_prof_abc(cur)
    # print "s_count {0:9} q_tot {1:9}".format(s_count, q_tots[itr])

    # print len(results)

    for i in range(len(results)):
        print ("{0:<9} {1:<9} {2:<9.4f} ".format(
            results[i][0],
            results[i][1],
            results[i][2]))
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__': main()
