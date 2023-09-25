# -*- coding:utf-8 -*-
'''
This module provides speech capabilities to a character playing "Don't starve together".
It acts as the startup file and orchestrates the ASR and game state monitoring.
'''

import threading
from Working_code import config as cf
from Working_code import state_changed as sc
from Working_code import asr as asr_module

# Set logger
logger = cf.logging.getLogger("dm.main")

if __name__ == "__main__":
    # Initialize ASR
    asr_instance = asr_module.listen_micr()
    asr_thread = threading.Thread(target=asr_instance.run)
    
    # Start ASR
    logger.info('Starting the ASR')
    asr_thread.start()
    
    # Start game state monitoring
    logger.info('Starting dm program')
    sc.state_changed_withoutHandler()
    
    # Terminate ASR
    logger.info('Requesting ASR termination')
    asr_instance.terminate()
    
    # Wait for ASR thread to finish
    logger.info('Waiting for ASR thread to join')
    asr_thread.join()
    
    logger.info('ASR thread stopped')
    logger.info('Stopping dm program, DONE')