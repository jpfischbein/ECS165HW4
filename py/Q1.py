'''
Created on Nov 29, 2016

@author: jphelps, Rochenko
'''

import sys
import psycopg2
import os

def connect():
    # user = 'jpfischbein'
    # user = os.environ['USER']
    user = "postgres"
    # print user
    try:
        conn = psycopg2.connect(dbname="postgres", user=user)
        return conn
    except:
        print "Failed to connect to the database"

def get_quarter_total(cur, qtr):
    cur.execute("SELECT COUNT(S.sid) "\
            "FROM Student S, "\
                "Course C "\
            "WHERE S.cid = C.cid AND C.quarter = %s;", [qtr])
    return float(cur.fetchone()[0])

def get_count_student_attempts_n_units_for_quarter(cur, units, qtr):
    cur.execute("SELECT COUNT(DISTINCT S.sid) "\
            "FROM Student S, "\
                "(SELECT sid, SUM(s.units) as sum "\
                "FROM Student s, Course c "\
                "WHERE s.cid = c.cid AND c.quarter = %s "\
                "GROUP BY sid, year) U "\
            "WHERE S.sid = U.sid AND U.sum = %s;", [qtr, units])
    return float(cur.fetchone()[0])

def main():
    conn = connect()
    cur = conn.cursor()

    #PRINT HEADER
    print ("{0:<9} {1:<9} {2:<9} {3:<9} {4:<9}"
        .format("Units", "Winter", "Spring", "Summer", "Fall"))

    # Get the Quarter Totals
    q_tots = []
    qtrs = [1,3,6,10]
    unitsPerQuarter = [0, 1, 1.5, 2, 3, 4, 5, 5.5, 6, 7, 7.5, 8, 8.5, 9, 9.5, 10, 11, 11.5, 12, 12.5, 13, 14, 15, 16, 17, 18, 19, 20, 21, 21.5, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]
    for qtr in qtrs:
        q_tots.append(get_quarter_total(cur, qtr))

    for units in unitsPerQuarter:
        percents = []
        itr = 0

        # Get the 
        for qtr in qtrs:
            s_count = get_count_student_attempts_n_units_for_quarter(cur, units, qtr)
            # print "s_count {0:9} q_tot {1:9}".format(s_count, q_tots[itr])
            percent = (s_count/q_tots[itr])*100
            percents.append(percent)
            itr += 1

        print ("{0:<9.1f} {1:<9.4f} {2:<9.4f} {3:<9.4f} {4:<9.4f}".format(
            units,
            percents[0], 
            percents[1], 
            percents[2], 
            percents[3]))

    # qtrs = [1,3,6,10]
    # units = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    # qtrTot = []
    # temp = []
    # perc = []
    # qtrUnit = []
    # prcnts = []
    # itr = 0
    # for qtr in qtrs:
    #     # GETS STUDENTS PER QUARTER ATTEMPTING UNITS
    #     # cur.execute("SELECT COUNT(sid) "\
    #     #             "FROM Student S, "\
    #     #                 "Course C "\
    #     #             "WHERE S.cid = C.cid AND C.quarter = %s;", [qtr])
    #     # qtrTot.append(float(cur.fetchone()[0]))
    #     for unit in units:
    #         # GETS STUDENTS PER QUARTER ATTEMPTING N UNITS
    #         cur.execute("SELECT COUNT(S.sid) "\
    #                     "FROM Student S, "\
    #                         "(SELECT sid, SUM(C.unitlow) "\
    #                         "FROM Student S, Course C "\
    #                         "WHERE S.cid = C.cid AND C.quarter = %s "\
    #                         "GROUP BY sid) U "\
    #                     "WHERE S.sid = U.sid AND U.sum = %s;", [qtr, unit])
    #         # cur.execute("SELECT quarter FROM Course GROUP BY quarter;")
    #         # print cur.fetchone()
    #         print "Students attempting %s units in %s quarter" % (unit, qtr)

    #         #GET PERCENTAGE
    #         stuff = float(cur.fetchone()[0])
    #         print stuff
    #         temp.append(stuff)

    #         otherStuff = (temp[unit-1]/qtrTot[itr])*10
    #         print otherStuff
    #         perc.append(otherStuff)
    #     #MAKE LISTS OF PERCENTAGE LISTS
    #     qtrUnit.append(temp)
    #     prcnts.append(perc)
    #     itr += 1

    # #PRINTS THE OUTPUT
    # print ("{0:<9} {1:<9} {2:<9} {3:<9} {4:<9}".format("Units", "Winter", "Spring", "Summer", "Fall"))
    # for i in range(20):
    #     print ("{0:<9.0f} {1:<9.3f} {2:<9.3f} {3:<9.3f} {0:<9.3f}".format(
    #         i,
    #         prcnts[0][i] * 100, 
    #         prcnts[1][i] * 100, 
    #         prcnts[2][i] * 100, 
    #         prcnts[3][i] * 100))
        # print "%s: %s,  %s,  %s,  %s" % [i, prcnts[0][i], prcnts[1][i], prcnts[2][i], prcnts[3][i]]

    # print "Quarter attempted totals"
    # print qtrTot
    # print "Number of students attempted specific units per quarter"
    # print qtrUnit
    # print "Percentages per unit per quarter"
    # print prcnts

if __name__ == '__main__': main()