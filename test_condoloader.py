import os
import unittest
import pathlib

import cx_sde
import condoloader


class CondoLoaderTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.datadirectory = os.path.join(pathlib.Path(__file__).parent
                                         ,'data'
                                         ,'testdata')

        self.sqldirectory = os.path.join(pathlib.Path(__file__).parent
                                        ,'sql_oracle'
                                        ,'definition')

        self.sdeconn = os.environ['SDEFILE']

        self.testtable = 'Condo'
        self.testfile  = 'condotestfile.csv'

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

        pass
        #sdereturn = cx_sde.execute_immediate(self.sdeconn,
        #                                     self.teardownsql)


    def test_aloadpluto(self):

        self.testtarget.loadpluto(self.datadirectory)

    def test_bloadcondo(self):

        self.testtarget.loadcondo(self.datadirectory)



if __name__ == '__main__':
    unittest.main()
