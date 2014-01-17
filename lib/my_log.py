# -*- coding: utf-8 -*-  

import os  
import logging  
import logging.config  
  
LOG_FILENAME = 'logging.conf'
os.chdir("/usr/home/zeyang/autoapi/config/")
logging.config.fileConfig(LOG_FILENAME)
logger = logging.getLogger("running error info")
