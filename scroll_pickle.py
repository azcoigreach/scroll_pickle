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

class Config(object):
    def __init__(self):
        self.debug = False

pass_config = click.make_pass_decorator(Config, ensure=True)

# Scoll Pickle

@click.option('--debug', is_flag=True,
              help='Debug Mode')
@click.option('--working_directory', '-w', type=click.Path())

def main(debug, working_directory):
    '''
    Scroll pickle data on Pimoroni Scroll Phat HD
    '''
    init(convert=True)
    if debug is True:
        logger.setLevel(logging.DEBUG)
        logger.debug('<<<DEBUG MODE>>>')
    else:
        logger.setLevel(logging.INFO)

    print("""
    Scroll pHAT HD: Advanced Scrolling

    Advanced scrolling example which displays a message line-by-line
    and then skips back to the beginning.

    Press Ctrl+C to exit.
    """)

    # Uncomment to rotate 180 degrees
    #scrollphathd.rotate(180)

    # Dial down the brightness
    scrollphathd.set_brightness(0.2)

    # If rewind is True the scroll effect will rapidly rewind after the last line
    rewind = True

    # Delay is the time (in seconds) between each pixel scrolled
    delay = 0.03

    # Change the lines below to your own message
    lines = ["In the old #BILGETANK we'll keep you in the know",
            "In the old #BILGETANK we'll fix your techie woes",
            "And we'll make things",
            "And we'll break things",
            "'til we're altogether aching",
            "Then we'll grab a cup of grog down in the old #BILGETANK"]

    # Determine how far apart each line should be spaced vertically
    line_height = scrollphathd.DISPLAY_HEIGHT + 2

    # Store the left offset for each subsequent line (starts at the end of the last line)
    offset_left = 0

    # Draw each line in lines to the Scroll pHAT HD buffer
    # scrollphathd.write_string returns the length of the written string in pixels
    # we can use this length to calculate the offset of the next line
    # and will also use it later for the scrolling effect.
    lengths = [0] * len(lines)

    for line, text in enumerate(lines):
        lengths[line] = scrollphathd.write_string(text, x=offset_left, y=line_height * line)
        offset_left += lengths[line]

    # This adds a little bit of horizontal/vertical padding into the buffer at
    # the very bottom right of the last line to keep things wrapping nicely.
    scrollphathd.set_pixel(offset_left - 1, (len(lines) * line_height) - 1, 0)

    while True:
        # Reset the animation
        scrollphathd.scroll_to(0, 0)
        scrollphathd.show()

        # Keep track of the X and Y position for the rewind effect
        pos_x = 0
        pos_y = 0

        for current_line, line_length in enumerate(lengths):
            # Delay a slightly longer time at the start of each line
            time.sleep(delay*10)

            # Scroll to the end of the current line
            for y in range(line_length):
                scrollphathd.scroll(1, 0)
                pos_x += 1
                time.sleep(delay)
                scrollphathd.show()

            # If we're currently on the very last line and rewind is True
            # We should rapidly scroll back to the first line.
            if current_line == len(lines) - 1 and rewind:
                for y in range(pos_y):
                    scrollphathd.scroll(-int(pos_x/pos_y), -1)
                    scrollphathd.show()
                    time.sleep(delay)

            # Otherwise, progress to the next line by scrolling upwards
            else:
                for x in range(line_height):
                    scrollphathd.scroll(0, 1)
                    pos_y += 1
                    scrollphathd.show()
                    time.sleep(delay)