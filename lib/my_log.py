# -*- coding: utf-8 -*-  

import os 
import logging  
import logging.config

from config import sysconfig 
  
LOG_FILENAME = 'logging.conf'
os.chdir(sysconfig._WORKSPACE + "/config")
logging.config.fileConfig(LOG_FILENAME)
logger = logging.getLogger("running info")
