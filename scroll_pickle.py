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
from scrollphathd.fonts import *

coloredlogs.install(level='DEBUG')
logger = logging.getLogger(__name__)

class Config(object):
    def __init__(self):
        self.debug = False

pass_config = click.make_pass_decorator(Config, ensure=True)


@pass_config
def refresh_data(config):
    config.p_data = 'hello'
    # config.p_data = pickle.load(config.file)
    config.p_data = str(config.p_data).encode('utf-8')
    logger.debug('p_data [%s] %s - refresh',type(config.p_data), config.p_data)
        

@pass_config
def display_data(config):
    logger.debug('p_data [%s] %s - display',type(config.p_data), config.p_data)
    scrollphathd.write_string(config.p_data, x=0, y=0, font=font5x7, brightness=0.3)
    scrollphathd.show()
    scrollphathd.scroll()


# Scoll Pickle
@click.command()
@click.option('--debug', is_flag=True,
              help='Debug Mode')
@click.argument('file', type=click.File('rb'))
@pass_config
def main(config, debug, file):
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
    config.file = file

    scrollphathd.rotate(180)
    scrollphathd.set_brightness(0.3)
    delay = 0.03

    while True:
        refresh_data()
        display_data()
        time.sleep(delay)