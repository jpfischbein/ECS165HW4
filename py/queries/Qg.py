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
    cur.execute("SELECT COUNT(DISTINCT sid) FROM Student")
    return int(cur.fetchone())

def get_students_switch_major(cur):
    cur.execute("SELECT s1.major as major, COUNT(DISTINCT s1.sid) as count "\
                "FROM Student s1, Student s2 "\
                "WHERE s1.sid=s2.sid AND s1.major!=s2.major AND "\
                    "(s1.year<s2.year OR (s1.year=s2.year AND s1.quarter<s2.quarter) "\
                "GROUP BY s1.major;")
    return cur.fetchall()

def get_students_switch_into_abc(cur):
    cur.execute("SELECT s1.major as major, COUNT(DISTINCT s1.sid) as count "\
                "FROM Student s1, Student s2 "\
                "WHERE s1.sid=s2.sid AND "\
                    "(s1.major!='ABC1' AND s1.major!='ABC2' AND s1.major!='ABCG') AND "\
                    "(s1.year<s2.year OR (s1.year=s2.year AND s1.quarter<s2.quarter) "\
                "GROUP BY s1.major;")

def main():
    start_time = time.time()
    conn = connect()
    cur = conn.cursor()

    #PRINT HEADER
    print ("{0:<9} {1:<9} {2:<9}".format("Major", "Percent Major", "Percent Total"))

    # Get the number of students
    total_students = get_total_number_of_students(cur)

    # Get number of students who change major, by old major
    total_switch_majors = get_students_switch_major(cur)

    # Get number of students who change major into ABC
    switch_major_abc = get_students_switch_into_abc(cur)

    for i in range(len(results)):
        print ("{0:<9} {1:<32} {2:<12.2f} ".format(results[i][0], results[i][1], results[i][2]))

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__': main()
