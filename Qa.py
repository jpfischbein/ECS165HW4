'''
Created on Nov 29, 2016

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
    cur.execute("SELECT COUNT(sid) "\
                "FROM "\
                    "(SELECT sid, SUM(s.units) as sum "\
                    "FROM Student s, Course c "\
                    "WHERE s.cid = c.cid "\
                    "GROUP BY sid, year, quarter) U "\
                "WHERE U.sum = %s;", [units])
    return float(cur.fetchone()[0])

def main():
    start_time = time.time()

    conn = connect()
    cur = conn.cursor()

    # Get the Quarter Totals
    q_tots = []
    qtrs = [1,3,6,10]
    # unitsPerQuarter = [0, 1, 1.5, 2, 3, 4, 5, 5.5, 6, 7, 7.5, 8, 8.5, 9, 9.5, 10, 11, 11.5, 12, 12.5, 13, 14, 15, 16, 17, 18, 19, 20, 21, 21.5, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]
    unitsPerQuarter = range(21)
    
    tot = get_quarter_total(cur)
    # print "total attemped = %s" % tot

    #PRINT HEADER
    print ("{0:<9} {1:<9}"
        .format("Units", "Percentages"))

    persum = 0;

    for units in unitsPerQuarter:
        if(units == 0):
            continue

        # Get the percentage of students attempting n units for quarter
        s_count = get_count_student_attempts_n_units_for_quarter(cur, units)
        # print "s_count {0:9} q_tot {1:9}".format(s_count, q_tots[itr])
        percent = (s_count/tot)*100
        persum += percent

        print ("{0:<9.1f} {1:<9.4f}".format(
            units,
            percent))

    print ("{0:<9} {1:<9.4f}".format(
            "Sum:", persum))
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__': main()
