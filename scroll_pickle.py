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
import threading

coloredlogs.install(level='DEBUG')
logger = logging.getLogger(__name__)

_local = threading.local()

class Config(object):
    def __init__(self):
        self.debug = False

pass_config = click.make_pass_decorator(Config, ensure=True)

def get_current_config(silent=False):
    try:
        return getattr(_local, 'stack')[-1]
    except (AttributeError, IndexError):
        if not silent:
            raise RuntimeError('There is no active click config.')

def push_config(config):
    """Pushes a new context to the current stack."""
    _local.__dict__.setdefault('stack', []).append(config)


def pop_config():
    """Removes the top level from the stack."""
    _local.stack.pop()


# def resolve_color_default(color=None):
#     """"Internal helper to get the default value of the color flag.  If a
#     value is passed it's returned unchanged, otherwise it's looked up from
#     the current context.
#     """
#     if color is not None:
#         return color
#     config = get_current_context(silent=True)
#     if ctx is not None:
#         return ctx.color



# @pass_config
def refresh_data():
    config = get_current_config(silent=True)
    logger.debug('config [%s] %s @ refresh_data',type(config), config)

    refresh = 5
    
    while True:
        config.p_data = pickle.load(config.file)
        config.p_data = str(config.p_data).encode('utf-8')
        logger.debug('p_data [%s] %s - refresh',type(config.p_data), config.p_data)

        time.sleep(refresh)
            

# @pass_config
def display_data(p_data='No Data '):
    config = get_current_config(silent=True)
    
    
    scrollphathd.rotate(180)
    scrollphathd.set_brightness(0.3)
    delay = 0.1
    
    scrollphathd.write_string(config.p_data, x=0, y=0, font=font5x7, brightness=0.5)
    
    while True:
        scrollphathd.show()
        scrollphathd.scroll()
        time.sleep(delay)


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

    # t1 = threading.Thread(target=refresh_data, args=(config, ))
    # t2 = threading.Thread(target=display_data, args=(config, ))
    t1 = threading.Thread(target=refresh_data)
    t2 = threading.Thread(target=display_data)

    t1.start()
    t2.start()

    logger.debug('Main Process Completed')