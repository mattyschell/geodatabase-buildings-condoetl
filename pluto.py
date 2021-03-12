import os
# pandas is in Propy env, see reqs
import pandas 
import urllib.request
import zipfile

# Authors: DuckDuckGo and StackOverflow.  Legends.

class Pluto(object):

    def __init__(self
                ,workdirectory):

        self.version = os.environ['PLUTOVERSION']
        self.url = 'https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyc_pluto_{0}_csv.zip'.format(self.version)
        self.workdirectory = workdirectory

        # set these once in init for cleaner setup teardown
        self.zippath  = os.path.join(self.workdirectory,'pluto.zip')
        # pluto_21v1.csv maybe determine this on the fly
        self.plutocsv  =  os.path.join(self.workdirectory
                                     ,'pluto_{0}.csv'.format(self.version))
        self.plutobbls = os.path.join(self.workdirectory,'plutobbls.csv') 
        self.condosqls = os.path.join(self.workdirectory,'plutocondo.sql') 

    def unzip(self):

        with zipfile.ZipFile(self.zippath, 'r') as zip_ref:
            myfiles = zip_ref.namelist()
            for myfile in myfiles:
                if myfile.endswith('.csv'):
                    zip_ref.extract(myfile, self.workdirectory)

    def download(self):        

        if os.path.exists(self.zippath):
            os.remove(self.zippath)

        if os.path.exists(self.plutocsv):
            os.remove(self.plutocsv)

        urllib.request.urlretrieve(self.url
                                  ,self.zippath)
        self.unzip()

        os.remove(self.zippath)

    def extractbbls(self):

        if os.path.exists(self.plutobbls):
            os.remove(self.plutobbls)

        cols = ['bbl']
        df_allbbls = pandas.read_csv(self.plutocsv, usecols=cols)

        # TODO: Learn how to filter pandas data frames

        df_allbbls.to_csv(self.plutobbls
                         ,columns=cols
                         ,index=False
                         ,header=False)

    def extractcondosql(self):

        condos = []
        with open(self.plutobbls) as f:
            for bbl in f:
                if (str(bbl)[6] == '7' and str(bbl)[7] == '5'):
                    # 1015377501.0
                    condos.append(str(bbl)[0:10])    

        kount = 0
        with open(self.condosqls, 'w') as f:
            for condo in condos:
                kount = kount + 1
                f.write('insert into pluto_load values({0});{1}'.format(condo,'\n'))            
            f.write('commit;{0}'.format('\n'))

        self.condocount = kount

    def cleanworkfiles(self):

        if os.path.exists(self.zippath):
            os.remove(self.zippath)

        if os.path.exists(self.plutocsv):
            os.remove(self.plutocsv)

        if os.path.exists(self.plutobbls):
            os.remove(self.plutobbls)

    def cleanallfiles(self):

        self.cleanworkfiles() 

        # this is the output, clean it in testing but not usually
        if os.path.exists(self.condosqls):
            os.remove(self.condosqls)

    def downloadextractcondosql(self):

        self.download()
        self.extractbbls()
        self.extractcondosql()
        self.cleanworkfiles()

        return self.condocount

