import os
import unittest
import pathlib
import shutil 

import cx_sde
import condoloader


class CondoLoaderTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.teardowntestdata = 'Y'

        self.datadirectory = os.path.join(pathlib.Path(__file__).parent
                                         ,'data'
                                         ,'testdata')

        self.sqldirectory = os.path.join(pathlib.Path(__file__).parent
                                        ,'sql_oracle'
                                        ,'definition')

        self.sdeconn = os.environ['SDEFILE']

        self.testtable = 'Condo'
        self.testcondofile  = 'condo_testfixtures.csv'
        self.testplutosql   = 'plutocondo_testfixtures.sql'

        shutil.copyfile(os.path.join(self.datadirectory, self.testcondofile)
                       ,os.path.join(self.datadirectory, 'condo.csv'))

        shutil.copyfile(os.path.join(self.datadirectory, self.testplutosql)
                       ,os.path.join(self.datadirectory, 'plutocondo.sql'))
                 
        self.testtarget = condoloader.CondoLoader()
        
        with open(os.path.join(self.sqldirectory,'teardown.sql'), 'r') as sqlfile:
            self.teardownsql = sqlfile.read() 

        sdereturn = cx_sde.execute_immediate(self.sdeconn
                                            ,self.teardownsql)

        with open(os.path.join(self.sqldirectory,'schema.sql'), 'r') as sqlfile:
            self.schemasql = sqlfile.read() 

        sdereturn = cx_sde.execute_immediate(self.sdeconn
                                            ,self.schemasql)

    @classmethod
    def tearDownClass(self):

        try:
            os.remove(os.path.join(self.datadirectory, 'condo.csv'))
        except:
            pass

        try:
            os.remove(os.path.join(self.datadirectory, 'plutocondo.sql'))
        except:
            pass

        if self.teardowntestdata == 'Y':

            sdereturn = cx_sde.execute_immediate(self.sdeconn
                                                ,self.teardownsql)


    def test_aloadpluto(self):

        self.testtarget.loadpluto(self.datadirectory)

        sql = """select count(*) from pluto_load"""

        sdereturn = cx_sde.selectavalue(self.sdeconn,
                                        sql)
    
        self.assertEqual(sdereturn, 5)

    def test_bloadcondo(self):

        self.testtarget.loadcondo(self.datadirectory)

        sql = """select count(*) from condo_load"""

        sdereturn = cx_sde.selectavalue(self.sdeconn,
                                        sql)
    
        self.assertEqual(sdereturn, 5)



if __name__ == '__main__':
    unittest.main()
