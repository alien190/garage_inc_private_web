import logging
from flask import current_app, g

class Logger():
    def __init__(self, filename, is_debug_enabled: bool):
        self.is_debug_enabled = is_debug_enabled
        logging.basicConfig(level=logging.INFO,filename=filename,filemode="a", format="%(asctime)s %(levelname)s %(message)s")

    def log_info(self, msg):
        if(self.is_debug_enabled):
            print(msg)
            logging.info(msg)
     
    def log_error(self, msg):
        print('Error:' + msg)
        logging.error(msg)


def get_logger():
    if 'logger' not in g:
        g.logger  = Logger(__name__+'.log', is_debug_enabled=current_app.config['IS_DEBUG_ENABLED'])
    
    return g.logger