# -*- coding: utf-8 -*-  

import os 
from config import sysconfig
import logging  
import logging.config  
  
LOG_FILENAME = 'logging.conf'
os.chdir(sysconfig._WORKSPACE + "/config")
logging.config.fileConfig(LOG_FILENAME)
logger = logging.getLogger("running error info")
