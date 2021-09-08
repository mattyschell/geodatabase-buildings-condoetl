import os
import logging
import time
import pathlib

import condo


def main(sourcesdeconn
        ,outputdir):

        sourcecondo = condo.Condo()

        sourcecondo.extracttofile('DOF_TAXMAP.Condo'
                                  ,outputdir)

        return sourcecondo.countcondos()  


if __name__ == '__main__':

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

    if not os.path.isfile(psourcesdeconn):
        logging.error("Condo source sde file {0} does not exist, "
                      "check SDEFILE environmental".format(psourcesdeconn))
        exit(retval)

    kount = main(psourcesdeconn
                ,datadir)

    # at this point our csv still has two bad duplicate types
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