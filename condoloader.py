import os
import arcpy
import csv

import cx_sde

class CondoLoader(object):

    def __init__(self):

        self.sdeconn = os.environ['SDEFILE']
        #load our extracted data into these two
        self.condoloadtable = 'condo_load'
        self.plutoloadtable = 'pluto_load'
        # final data will be pushed here from 2 load tables above
        self.condotable = 'condo'
        # expected inputs extracted by previous modules into any "data" dir
        self.plutosql = 'plutocondo.sql'
        self.condocsv = 'condo.csv'

    def delete(self
              ,tablename):

        sql = 'delete from {0}'.format(tablename)

        sdereturn = cx_sde.execute_immediate(self.sdeconn
                                            ,sql)

    def loadpluto(self
                 ,datadir):

        self.delete(self.plutoloadtable)

        with open(os.path.join(datadir, self.plutosql), 'r') as f:
            sqls = f.readlines() 

        for line in sqls:
            sdereturn = cx_sde.execute_immediate(self.sdeconn
                                                ,line.strip().rstrip(';'))


    def loadcondo(self
                 ,datadir):

        self.delete(self.condoloadtable)

        kount = 0
        sqls = []
        with open(os.path.join(datadir, self.condocsv), 'r') as csvfile:
            condocsvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            
            for row in condocsvreader:
                if kount == 0:
                    kount += 1
                else:
                    kount += 1
                    sql = 'insert into {0} values({1},{2})'.format(self.condoloadtable
                                                                 ,row[1]
                                                                 ,row[2])
                    sdereturn = cx_sde.execute_immediate(self.sdeconn
                                                        ,sql)        

        


    
    