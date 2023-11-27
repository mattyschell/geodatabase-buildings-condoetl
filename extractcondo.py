import os
import sys
import logging
import time
import pathlib

import condo


def main(outputdir
        ,sourcelayer): 

        # sourcelayer is either (sdefile.sde/+)  this: <<schema.table>>
        # or          (http:/url/FeatureServer+) this: <<1>>

        sourcecondo = condo.Condo()

        sourcecondo.extracttofile(sourcelayer
                                 ,outputdir)

        return sourcecondo.countcondos()  


if __name__ == '__main__':

    if len(sys.argv) > 1:
        psourcelayer =  sys.argv[1]
    else:
        psourcelayer = 'DOF_TAXMAP.CONDO'
         
    psourcesdeconn = os.environ['SDEFILE']
        
    timestr = time.strftime("%Y%m%d-%H%M%S")

    retval = 1

    try:
        targetlog = os.path.join(os.environ['TARGETLOGDIR'] 
                                ,'extractcondo-{0}.log'.format(timestr)) 
    except:
        targetlog = os.path.join(os.getcwd() 
                                ,'extractcondo-{0}.log'.format(timestr))

    logging.basicConfig(filename=targetlog
                       ,level=logging.INFO)

    datadir = os.path.join(pathlib.Path(__file__).parent
                          ,'data')

    kount = main(datadir
                ,psourcelayer)

    # at this point our csv still likely has two bad duplicate types
    # condo_base_bbl condo_billing_bbl
    #      A               X
    #      A               X
    #      B               Y
    #      B               Z

    if (kount == 0 or kount is None):
        logging.error('Failed to extract any condos')
    else:
        logging.info('Successfully extracted {0} bbls to data directory'.format(kount))
        retval = 0

    exit(retval)