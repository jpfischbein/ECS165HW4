
'''
Created on Nov 29, 2016

@author: jphelps
'''

import sys
import os
from os import listdir
from os.path import isfile, join
import csv
import re
import psycopg2
import time

clist = []

def insertValues(cur, conn, crsdict, mlist, slist):
    #PREPARE COURSE INSERT
    # print crsdict['cid']
    # cur.execute("""INSERT INTO Course(cid,year,quarter,subject,crse,section,unitlow,unithigh) VALUES (%(cid)s,%(year)s,%(quarter)s,%(subject)s,%(crse)s,%(section)s,%(unitlow)s,%(unithigh)s);""", crsdict)
    command = "INSERT INTO Course(cid,year,quarter,subject,crse,section,unitlow,unithigh) VALUES (%(cid)s,%(year)s,%(quarter)s,\'%(subject)s\',%(crse)s,%(section)s,%(unitlow)s,%(unithigh)s); " % crsdict
    
    # print command 
    # print crsdict['cid']

    #PREPARE MEETING INSERTS
    for mdict in mlist:
        #Parse instructor
        if(mdict['instructor'] == ''):
            inst = 'null'
        else:
            inst = mdict['instructor'].replace(',','')
            if(inst.find('\'') != -1):
                # print inst
                inst = inst.replace('\'','')
            # print inst
        #Parse type
        if(mdict['type'] == ''):
            typ = 'null'
        else:
            typ = mdict['type']
        #Parse days
        if(mdict['days'] == ''):
            m = 'False'
            t = 'False'
            w = 'False'
            r = 'False'
            f = 'False'
            s = 'False'
        else:
            m = 'FALSE'
            t = 'FALSE'
            w = 'FALSE'
            r = 'FALSE'
            f = 'FALSE'
            s = 'FALSE'
        if(mdict['days'].find('M') != -1):
            m = 'TRUE'
        if(mdict['days'].find('T') != -1):
            t = 'TRUE'
        if(mdict['days'].find('W') != -1):
            w = 'TRUE'
        if(mdict['days'].find('R') != -1):
            r = 'TRUE'
        if(mdict['days'].find('F') != -1):
            f = 'TRUE'
        if(mdict['days'].find('S') != -1):
            s = 'TRUE'
        #Parse start and end times
        time = mdict['time']
        if(time == ''):
            start = -1
            end = -1
        else:
            # print time
            # print len(time)
            if((time.find('AM') != -1) and (time.find('PM') != -1)):
                if(len(time) == 17):
                    start = time[0]
                    start += time[2:4]
                    # print start
                    end = int(time[10])
                    if (end != 12):
                        end += 12
                    end = str(end)
                    end += time[12:14]
                    # print end
                elif(len(time) == 19):
                    start = time[0:2]
                    start += time[3:5]
                    # print start
                    end = int(time[11:13])
                    if (end != 12):
                        end += 12
                    end = str(end)
                    end += time[14:16]
                    # print end
                else:
                    if(time[1] == ':'):
                        start = time[0]
                        start += time[2:4]
                        # print start
                        end = int(time[10:12])
                        if(end != 12):
                            end += 12
                        end = str(end)
                        end += time[13:15]
                        # print end
                    else:
                        start = time[0:2]
                        start += time[3:5]
                        # print start
                        end = int(time[11])
                        if(end != 12):
                            end += 12
                        end = str(end)
                        end += time[13:15]
                        # print end
            elif(time.find('PM') != -1):
                if(len(time) == 17):
                    start = int(time[0])
                    if(start != 12):
                        start += 12
                    start = str(start)
                    start += time[2:4]
                    # print start
                    end = int(time[10])
                    if (end != 12):
                        end += 12
                    end = str(end)
                    end += time[12:14]
                    # print end
                elif(len(time) == 19):
                    start = int(time[0:2])
                    if(start != 12):
                        start += 12
                    start = str(start)
                    start += time[3:5]
                    # print start
                    end = int(time[11:13])
                    if (end != 12):
                        end += 12
                    end = str(end)
                    end += time[14:16]
                    # print end
                else:
                    if(time[1] == ':'):
                        start = int(time[0])
                        if(start != 12):
                            start += 12
                        start = str(start)
                        start += time[2:4]
                        # print start
                        end = int(time[10:12])
                        if(end != 12):
                            end += 12
                        end = str(end)
                        end += time[13:15]
                        # print end
                    else:
                        start = int(time[0:2])
                        if(start != 12):
                            start += 12
                        start = str(start)
                        start += time[3:5]
                        # print start
                        end = int(time[11])
                        if(end != 12):
                            end += 12
                        end = str(end)
                        end += time[13:15]
                        # print end
            else:
                if(len(time) == 17):
                    start = time[0]
                    start += time[2:4]
                    # print start
                    end = time[10]
                    end += time[12:14]
                    # print end
                elif(len(time) == 19):
                    start = time[0:2]
                    start += time[3:5]
                    # print start
                    end = time[11:13]
                    end += time[14:16]
                    # print end
                else:
                    if(time[1] == ':'):
                        start = time[0]
                        start += time[2:4]
                        # print start
                        end = time[10:12]
                        end += time[13:15]
                        # print end
                    else:
                        start = time[0:2]
                        start += time[3:5]
                        # print start
                        end = time[11]
                        end += time[13:15]
                        # print end
        #Parse building
        if(mdict['building'] == ''):
            build = 'null'
        else:
            build = mdict['building']
        #Parse room
        if(mdict['room'] == ''):
            room = -1
        else:
            room = mdict['room']
        # cur.execute("""INSERT INTO Meeting(cid,instructor,type,mon,tues,wed,thur,fri,sat,starttime,endtime,building,room) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""", (crsdict['cid'], inst, typ, m, t, w, r, f, s, start, end, build, room))
        command += "INSERT INTO Meeting(cid,instructor,type,mon,tues,wed,thur,fri,sat,starttime,endtime,building,room) VALUES (%s,\'%s\',\'%s\',%s,%s,%s,%s,%s,%s,%s,%s,\'%s\',%s); " % (crsdict['cid'], inst, typ, m, t, w, r, f, s, start, end, build, room)

    #PREPARE STUDENT INSERT
    for sdict in slist:
        #Parse name
        name = sdict['surname']
        if(name.find('\'') != -1):
            # print name
            name = name.replace('\'','')
            # print name
        #Parse grade
        grad = sdict['grade']
        grade = 'null'
        if (grad == 'A+') or (grad == 'A'):
            grade = 4.0
        elif (len(grad) == 1 or len(grad) == 2):
            if (grad[0] == 'B'):
                grade = 3.0
            elif (grad[0] == 'C'):
                grade = 2.0
            elif (grad[0] == 'D'):
                grade = 1.0
            elif (grad == 'F'):
                grade = 0.0
            if (len(grad) == 2 and (grade != 'null') and (grad[1] == '+')):
                grade += 0.3
            if (len(grad) == 2 and (grade != 'null') and (grad[1] == '-')):
                grade -= 0.3
        #Parse units
        if(sdict['units'] == ''):
            unts = 0
        else:
            unts = sdict['units']
        #Parse email
        email = sdict['email']
        if(email.find('\'') != -1):
            # print email
            email = email.replace('\'','')
            # print email
        # cur.execute("""INSERT INTO Student(cid,sid,surname,prefname,level,units,class,major,grade,status,email) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""", (crsdict['cid'], sdict['sid'], sdict['surname'], sdict['prefname'], sdict['level'], unts, sdict['class'], sdict['major'], grade, sdict['status'], sdict['email']))
        command += "INSERT INTO Student(cid,sid,surname,prefname,level,units,class,major,grade,status,email) VALUES (%s,%s,\'%s\',\'%s\',\'%s\',%s,\'%s\',\'%s\',%s,\'%s\',\'%s\'); " % (crsdict['cid'], sdict['sid'], name, sdict['prefname'], sdict['level'], unts, sdict['class'], sdict['major'], grade, sdict['status'], email)
        
    #SEND COMMAND TO DATABASE
    cur.execute(command)
    # cur.executemany(command, ())
    # conn.commit()
    # print "EXECUTED"
    # print command

    # print '\n'
    # print command 

        # print mdict['days']

def parse(cur, conn, filepath):
    keys = (1,2,3,4,5,6,7,8,9,10,11)
    data = False
    valid = True
    mlist = []
    slist = []
    # clist = []
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile, keys, 'gweem', 'none')
        for row in reader:
            if((valid == False) and (row[1] != 'CID')):
                # print ">>>>>>>>Invalid and not CID"
                continue
            if(row[2] != 'none'):
                # print ">>>>>>>>Row is not just quotes"
                #NEXT IS COURSE DATA
                if(row[1] == 'CID'):
                    # print "COURSE"
                    Type = 1
                    valid = True
                    continue
                #NEXT IS MEETING DATA
                if(row[1] == 'INSTRUCTOR(S)'):
                    # print "MEETING"
                    Type = 2
                    continue
                #NEXT IS STUDENT DATA
                if(row[1] == 'SEAT'):
                    # print "STUDENT"
                    Type = 3
                    continue
                # print "DATA"
                data = True
                #COURSE DATA
                if(Type == 1):
                    cid = row[1]
                    if(len(row[6]) > 1):                    
                        if(len(row[6]) == 14):
                            coursedict = ({"cid":row[1],"year":row[2][:4],"quarter":row[2][4:], \
                                "subject":row[3],"crse":row[4],"section":row[5],"unitlow":row[6][0], \
                                "unithigh":row[6][8:10]})
                            continue
                        else:
                            coursedict = ({"cid":row[1],"year":row[2][:4],"quarter":row[2][4:], \
                                "subject":row[3],"crse":row[4],"section":row[5],"unitlow":row[6][0], \
                                "unithigh":row[6][8]})
                            continue
                    else:
                        coursedict = ({"cid":row[1],"year":row[2][:4],"quarter":row[2][4:], \
                            "subject":row[3],"crse":row[4],"section":row[5],"unitlow":row[6][0], \
                            "unithigh":row[6][0]})
                        continue
                #MEETING DATA
                if(Type == 2):
                    meetdict = ({"cid":cid,"instructor":row[1],"type":row[2], \
                        "days":row[3],"time":row[4],"building":row[5],"room":row[6]})
                    mlist.append(meetdict)
                    continue
                #STUDENT DATA
                if(Type == 3):
                    studDict = ({"cid":cid,"seat":row[1],"sid":row[2], \
                        "surname":row[3],"prefname":row[4],"level":row[5], \
                        "units":row[6],"class":row[7],"major":row[8],"grade":row[9], \
                        "status":row[10],"email":row[11]})
                    slist.append(studDict)
                    continue
            #The line is just ""
            else:
                # print ">>>>>>>>Row is just quotes"
                if(data == False):
                    # print ">>>>>>>>Row should be data: INVALID"
                    mlist = []
                    slist = []
                    valid = False
                    continue
                data = False
                if(Type == 3):
                    # print cid
                    clist.append(cid)
                    insertValues(cur, conn, coursedict, mlist, slist)
                    mlist = []
                    slist = []
    # print len(clist)

def makeTables(cur):
    cur.execute("BEGIN; CREATE TABLE Course(cid INT, year INT, quarter INT," \
        " subject CHAR(3), crse INT, section INT, unitlow INT, unithigh INT);" \
        "CREATE TABLE Meeting(cid INT, instructor CHAR(32), type CHAR(32),"\
        " mon BOOLEAN, tues BOOLEAN, wed BOOLEAN, thur BOOLEAN, fri BOOLEAN,"\
        " sat BOOLEAN, starttime INT, endtime INT, building CHAR(16), room INT);" \
        "CREATE TABLE Student(cid INT, sid INT, surname CHAR(16),"\
        " prefname CHAR(16), level CHAR(8), units FLOAT, class CHAR(8),"\
        " major CHAR(4), grade DOUBLE PRECISION, status CHAR(8), email CHAR(64)); COMMIT;")    

def connect():
    # user = 'jpfischbein'
    # user = os.environ['USER']
    user = "postgres"
    try:
        conn = psycopg2.connect(dbname="postgres", user=user)
        return conn
    except:
        print "Failed to connect to the database"

def main(argv):
    if (2 != len(sys.argv)):
        print "Incorrect number of arguments"
        return 0

    start_time = time.time()

    conn = connect()
    cur = conn.cursor()
    makeTables(cur)

    path = str(sys.argv[1])
    csvfiles = [f for f in listdir(path) if isfile(join(path, f))]
    # print len(csvfiles)
    slash = '/'
    for csvfile in csvfiles:
        if (0 == csvfile):
            print "File not valid"
        else:
            # print csvfile
            pathseq = (path, csvfile)
            csvfilepath = slash.join(pathseq)
            parse(cur, conn, csvfilepath)

    # print len(clist)

    # parse(cur, conn, 'Grades/1995_Q4.csv')
    # print len(clist)

    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__': main(sys.argv[1:])
