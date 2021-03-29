import os
import logging
import time
import pathlib

import condoloader


def main(datadir):

    target = condoloader.CondoLoader()

    if target.databaseisready():

        target.loadpluto_load(datadir)
        target.loadcondo_load(datadir)
        target.loadcondo()

    else:

        logging.error('Target database isnt ready, check SDECONN environmental and work tables')
        return 0

    return target.bblcount


if __name__ == '__main__':

    timestr = time.strftime("%Y%m%d-%H%M%S")

    try:
        targetlog = os.path.join(os.environ['TARGETLOGDIR'] 
                                ,'loadcondo-{0}.log'.format(timestr)) 
    except:
        targetlog = os.path.join(os.getcwd() 
                                ,'loadcondo-{0}.log'.format(timestr))

    logging.basicConfig(filename=targetlog
                       ,level=logging.INFO)

    pdatadir = os.path.join(pathlib.Path(__file__).parent
                           ,'data')

    kount = main(pdatadir)

    if (kount == 0 or kount is None):
        logging.error('Failed to load any condos')
        retval = 1
    else:
        logging.info('Successfully loaded {0} bbls to the condo table'.format(kount))
        retval = 0

    exit(retval)