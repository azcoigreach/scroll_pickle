#!/usr/bin/env python2
import sys
import os
from os import path
import time
from datetime import datetime, timedelta
import pickle
import json
import string
import logging
import coloredlogs
import click
from colorama import init, Fore
import scrollphathd


coloredlogs.install(level='DEBUG')
logger = logging.getLogger(__name__)


# Scoll Pickle
@click.command()
@click.option('--debug', is_flag=True,
              help='Debug Mode')
@click.argument('file', type=click.File('rb'))

def main(debug, file):
    '''
    ** Scroll pickle data on Pimoroni Scroll Phat HD. **

    \b
    scroll_pickle [filename].pickle

    \b
    ** Requires ScrollPhatHD hardware with RaspberryPi **
    '''
    init(convert=True)
    if debug is True:
        logger.setLevel(logging.DEBUG)
        logger.debug('<<<DEBUG MODE>>>')
    else:
        logger.setLevel(logging.INFO)
    
    scrollphathd.rotate(180)
    scrollphathd.set_brightness(0.2)
    delay = 0.03


    def refresh_data():
        p_data = pickle.load(file)

        lines = []
        logger.debug('p_data type: %s',type(p_data))
        
        if type(p_data) is list:
            logger.debug('Process p_data list')
            for i in iter(p_data):
                for key, value in i.items():
                    if key == '_id':
                        id_value = value
                        # logger.debug(id_value)
                    if key == 'count':
                        count_value = value
                        # logger.debug(count_value)

                data = str('%s : %s') % id_value, count_value
                logger.debug('data: [%s] %s', type(data), data)
                lines.append(data)
                
        else:
            logger.debug('single line')
            lines.append(str(p_data) + ' ')
        
        logger.debug('words list: [%s] %s', type(lines), lines)
        
        scrollphathd.write_string(lines, x=0, y=0, font=font5x7, brightness=0.5)

    while True:
        refresh_data()

        scrollphathd.show()
        scrollphathd.scroll()
        time.sleep(delay)