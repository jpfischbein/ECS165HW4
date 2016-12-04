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

def get_total_number_of_students(cur):
    cur.execute("SELECT COUNT(DISTINCT sid) FROM Student;")
    return float(cur.fetchone()[0])

def get_students_switch_major(cur, major):
    cur.execute("SELECT COUNT(DISTINCT s1.sid) as count "\
                "FROM Student s1, Student s2, Course c1, Course c2 "\
                "WHERE s1.sid=s2.sid AND s1.major=%s AND s1.cid=c1.cid AND s2.cid=c2.cid AND "\
                    "(c1.year<c2.year OR (c1.year=c2.year AND c1.quarter<c2.quarter))"\
                ";", [major])
    return float(cur.fetchone()[0])

def get_students_switch_into_abc(cur):
    cur.execute("SELECT * "\
                "FROM ("
                    "SELECT s1.major as major, COUNT(DISTINCT s1.sid) as count "\
                    "FROM Student s1, Student s2, Course c1, Course c2 "\
                    "WHERE s1.sid=s2.sid AND s1.cid=c1.cid AND s2.cid=c2.cid AND "\
                        "(s1.major!='ABC1' AND s1.major!='ABC2' AND s1.major!='ABCG') AND "\
                        "(s2.major='ABC1' OR s2.major='ABC2' OR s2.major='ABCG') AND "\
                        "(c1.year<c2.year OR (c1.year=c2.year AND c1.quarter<c2.quarter)) "\
                    "GROUP BY s1.major"\
                    ") sm "\
                "ORDER BY count;")
    return cur.fetchall()

def main():
    start_time = time.time()
    conn = connect()
    cur = conn.cursor()

    #PRINT HEADER
    print ("{0:<9} {1:<15} {2:<9}".format("Major", "Percent Major", "Percent Total"))

    # Get the number of students
    total_students = get_total_number_of_students(cur)

    # Get number of students who change major into ABC
    switch_major_abc = get_students_switch_into_abc(cur)

    for i in range(5):
        abc_switch = switch_major_abc[i][1]
        print abc_switch
        major_switch = get_students_switch_major(cur, switch_major_abc[i][0])
        major_percent = float(abc_switch/major_switch)*100
        total_percent = float(abc_switch/total_students)*100
        print ("{0:<9} {1:<15.2f} {2:<12.2f} ".format(
            switch_major_abc[i][0], major_percent, total_percent))

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__': main()
