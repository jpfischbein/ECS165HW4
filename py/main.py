#!/usr/bin/python2.7

'''
Created on Nov 28, 2016

@author: Rochenko
'''
import psycopg2

def createPickupsTable(cur):
    cur.execute("CREATE TABLE Boat(model CHAR(64), city DOUBLE PRECISION, highway DOUBLE PRECISION, passengers INT, cargo INT, towing INT, msrp INT);")

def initDB(cur):
    pickupdict = ({"model":"truckA1", "city":"20", "highway":"23", "passengers":"2", "cargo":"120", "towing":"1500", "msrp":"7000"}, {"model":"truckB1", "city":"24", "highway":"28", "passengers":"4", "cargo":"140", "towing":"2400", "msrp":"10000"}, {"model":"truckB2", "city":"30", "highway":"35", "passengers":"4", "cargo":"150", "towing":"2500", "msrp":"12000"})
    cur.executemany("""INSERT INTO Boat(model,city,highway,passengers,cargo,towing,msrp) VALUES (%(model)s,%(city)s,%(highway)s,%(passengers)s,%(cargo)s,%(towing)s,%(msrp)s)""", pickupdict)

def connect():
    try:
        conn = psycopg2.connect(dbname="postgres", user="postgres")
        cur = conn.cursor()
        return cur
    except:
        try: 
            conn = psycopg2.connect(dbname="postgres", user="ijohndoe")
            cur = conn.cursor()
            return cur
        except:
            try:
                conn = psycopg2.connect(dbname="postgres", user="jphelps")
                cur = conn.cursor()
                return cur
            except:
                print "Failed to connect to the database"

def printPickups(cur):
    cur.execute("""SELECT * from Boat""")
    rows = cur.fetchall()
    print "\nShow me the databases:\n"
    for row in rows:
        print "   ", row[0] 

def main():      
    try:
        cur = connect()
        createPickupsTable(cur)
        initDB(cur)
        printPickups(cur)
    except:
        print "Fbase"

if __name__ == '__main__': main()

