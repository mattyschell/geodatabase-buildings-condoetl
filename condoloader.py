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

    def databaseisready(self):

        for tablename in [self.condoloadtable
                         ,self.plutoloadtable
                         ,self.condotable]:
            
            sql = 'select count(*) from {0} where 1=1 '.format(tablename)

            
            try:
                kount = cx_sde.selectavalue(self.sdeconn
                                           ,sql)  
            except:
                print('failed to execute {0}'.format(sql))
                return False
        
        return True

    def delete(self
              ,tablename):

        sql = 'delete from {0}'.format(tablename)

        sdereturn = cx_sde.execute_immediate(self.sdeconn
                                            ,sql)

    def loadpluto_load(self
                      ,datadir):

        self.delete(self.plutoloadtable)

        with open(os.path.join(datadir, self.plutosql), 'r') as f:
            sqls = f.readlines() 

        sdereturn = cx_sde.execute_statements(self.sdeconn
                                             ,sqls)

    def loadcondo_load(self
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
                    sqls.append('insert into {0} values({1},{2}) '.format(self.condoloadtable
                                                                         ,row[1]
                                                                         ,row[2]))
        sdereturn = cx_sde.execute_statements(self.sdeconn
                                             ,sqls)        
 
    def loadcondo(self):

        self.delete(self.condotable)

        # insert into condo
        #   (condo_base_bbl
        #   ,condo_billing_bbl)
        # select distinct 
        #    a.condo_base_bbl
        #   ,a.condo_billing_bbl 
        # from 
        #    condo_load a
        # join 
        #    pluto_load b
        # on 
        # a.condo_billing_bbl = b.bbl
        
        sql  = 'insert into {0} '.format(self.condotable) 
        sql += '(condo_base_bbl ,condo_billing_bbl) '
        sql += 'select distinct a.condo_base_bbl, a.condo_billing_bbl '
        sql += 'from {0} a '.format(self.condoloadtable)
        sql += 'join {0} b '.format(self.plutoloadtable)
        sql += 'on a.condo_billing_bbl = b.bbl '
              
        sdereturn = cx_sde.execute_immediate(self.sdeconn
                                            ,sql)  

        sql = 'select count(*) from {0}'.format(self.condotable)

        self.bblcount = cx_sde.selectavalue(self.sdeconn
                                           ,sql)     


    
    