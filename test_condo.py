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
        self.badgeodatabase = os.path.join(os.path.abspath(self.datadirectory)
                                          ,'doesnotexist.gdb')        
        self.testtable = 'Condo'

    @classmethod
    def tearDownClass(self):
        
        if self.teardowntestdata == 'Y':

            os.remove(os.path.join(self.datadirectory
                                  ,'condo.csv'))

            os.remove(os.path.join(self.datadirectory
                                  ,'condo.csv.xml'))

    
    def test_abadsde(self):

        os.environ["SDEFILE"] = self.badgeodatabase

        badgdb = False

        try:
            self.testcondo = condo.Condo()
        except:
            badgdb = True

        self.assertTrue(badgdb)

    def test_bextract(self):

        os.environ["SDEFILE"] = self.testgeodatabase
        self.testcondo = condo.Condo()

        self.testcondo.extracttofile(self.testtable
                                    ,self.datadirectory)

        self.assertEqual(self.testcondo.countcondos(), 5)


        # if I decide to clean up weird values in the csv
        # that test goes here next


if __name__ == '__main__':
    unittest.main()
