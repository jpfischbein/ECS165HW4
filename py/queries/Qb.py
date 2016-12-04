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

def get_average_gpa_student_attempts_n_units_for_quarter(cur, units):
    cur.execute("SELECT AVG(GPA) "\
                "FROM "\
                    "(SELECT sid, SUM(s.units) as sum, AVG(grade) as GPA "\
                    "FROM Student s, Course c "\
                    "WHERE s.cid = c.cid AND grade != 'nan' "\
                    "GROUP BY sid, year, quarter) U "\
                "WHERE U.sum = %s "\
                "GROUP BY sum;", [units])
    return float(cur.fetchone()[0])

def main():
    start_time = time.time()
    conn = connect()
    cur = conn.cursor()

    # Get the Quarter Totals
    unitsPerQuarter = range(1, 21)
    
    #PRINT HEADER
    print ("{0:<9} {1:<9}".format("Units", "Average GPA"))

    for units in unitsPerQuarter:

        # Get the percentage of students attempting n units for quarter
        ave_gpa = get_average_gpa_student_attempts_n_units_for_quarter(cur, units)

        print ("{0:<9.0f} {1:<9.2f}".format(units, ave_gpa))

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__': main()
