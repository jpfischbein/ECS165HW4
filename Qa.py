'''
Created on Nov 29, 2016

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

def get_quarter_total(cur):
    cur.execute("SELECT COUNT(S.sid) "\
                "FROM Student S, "\
                    "(SELECT sid, SUM(s.units) as sum "\
                    "FROM Student s, Course c "\
                    "WHERE s.cid = c.cid "\
                    "GROUP BY sid, year, quarter) U "\
                "WHERE S.sid = U.sid AND U.sum > 0;")
    return float(cur.fetchone()[0])

def get_count_student_attempts_n_units_for_quarter(cur, units):
    cur.execute("SELECT COUNT(S.sid) "\
                "FROM Student S, "\
                    "(SELECT sid, SUM(s.units) as sum "\
                    "FROM Student s, Course c "\
                    "WHERE s.cid = c.cid "\
                    "GROUP BY sid, year, quarter) U "\
                "WHERE S.sid = U.sid AND U.sum = %s;", [units])
    return float(cur.fetchone()[0])

def main():
    start_time = time.time()

    conn = connect()
    cur = conn.cursor()
    
    tot = get_quarter_total(cur)
    # print "total attemped = %s" % tot

    #PRINT HEADER
    print ("{0:<9} {1:<15}".format("Units", "Percentages"))

    persum = 0;

    for units in range(1, 21):

        # Get the percentage of students attempting n units for quarter
        s_count = get_count_student_attempts_n_units_for_quarter(cur, units)
        percent = (s_count/tot)*100
        persum += percent

        print ("{0:<9.0f} {1:<9.2f}".format(units, percent))

    print ("{0:<9} {1:<9.4f}".format("Sum:", persum))
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__': main()
