import os
import unittest
import pathlib

import condo


class CondoTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.teardowntestdata = 'Y'

        # mock the SDE environmental ala
        #C:\matt_projects\geodatabase-buildings-condoetl\data\testdata\testdata.gdb\Condo
        self.datadirectory = os.path.join(pathlib.Path(__file__).parent
                                         ,'data'
                                         ,'testdata')
        self.testgeodatabase = os.path.join(os.path.abspath(self.datadirectory)
                                           ,'testdata.gdb')        
        os.environ["SDEFILE"] = self.testgeodatabase

        self.testtable = 'Condo'
        self.testcondo = condo.Condo()


    @classmethod
    def tearDownClass(self):
        
        if self.teardowntestdata == 'Y':

            os.remove(os.path.join(self.datadirectory
                                  ,'condo.csv'))

            os.remove(os.path.join(self.datadirectory
                                  ,'condo.csv.xml'))

    def test_aextract(self):

        self.testcondo.extracttofile(self.testtable
                                    ,self.datadirectory)

        self.assertEqual(self.testcondo.countcondos(), 5)

        # if I decide to clean up weird values in the csv
        # that test goes here next


if __name__ == '__main__':
    unittest.main()
