#!/usr/bin/env python

__author__ = "Christoph Pranzl"
__copyright__ = "Copyright 2022, Christoph Pranzl"
__credits__ = ["Christoph Pranzl"]
__license__ = "GPL-3.0"
__version__ = "0.0.1"
__maintainer__ = "Christoph Pranzl"
__email__ = "christoph.pranzl@pranzl.net"
__status__ = "prototype"

"""
SYNOPSIS
    100prisoners [-b N, --boxes N] [-p N, --picks N] [-h,--help] [-v,--verbose] [--version]
DESCRIPTION
    Simulates the 'Prisoners boxes' riddle
EXAMPLES
    100prisoners -b 100 -p 50
EXIT STATUS
    TODO: List exit codes
"""

import sys, os, traceback, optparse, subprocess, time
import random
from datetime import datetime


def logwrite(message):
    """ Writes message and date to logfile """
    logfile = open('100prisoners.log', 'a')
    logfile.write(message + ' ' + datetime.utcnow().isoformat() + '\n')
    logfile.close


def create_boxes(amount):
    """ Create a nested dictionary which simulates boxes with a label on the 
        outside and a note with another number on the inside"""
    notes = list(range(amount))
    random.shuffle(notes)
    boxes = {}
    for i in range(amount):
        boxes[i] = {'label': i, 'note': notes[i], 'ring': 0}
    return boxes

def create_picks(amount):
    """ TODO """
    picks = list(range(amount))
    random.shuffle(picks)
    return picks


def main():
    """ TODO """
    global options, args

    boxes = create_boxes(options.boxes)

    picks = create_picks(options.boxes)
    pick = 0
    
    ring = 1
    
    while pick <= options.picks:
        start_box = picks[pick]
        if boxes[start_box]['ring'] != 0:
            """ Box is part of a found ring, a prisoner wouldn't pick a box 
                already checked"""
            pick += 1
            print(f"Box: {start_box} already checked")
        else:
            """ Box is not part of a found ring """
            pick += 1
            boxes[start_box]['ring'] = ring
            print(f"Pick: {pick}, Box: {start_box}, Note: {boxes[start_box]['note']}, Ring: {ring}")
            
            next_box = boxes[start_box]['note']
            pick += 1
            
            if next_box == start_box:
                """ Edgecase ring length 1 """
                boxes[next_box]['ring'] = ring
                print(f"Pick: {pick}, Box: {next_box}, Note: {boxes[next_box]['note']}, Ring: {ring}")
                ring += 1
            else:
                """ Ring length > 1 """
                while (next_box != start_box) and (pick <= options.picks):
                    boxes[next_box]['ring'] = ring
                    print(f"Pick: {pick}, Box: {next_box}, Note: {boxes[next_box]['note']}, Ring: {ring}")
                    
                    next_box = boxes[next_box]['note']
                    pick += 1
                boxes[next_box]['ring'] = ring
                ring += 1
    
    
if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'],
            version=globals()['__version__']
        )
        parser.add_option (
            '-b', '--boxes', dest='boxes', 
            default=100, type='int', help='number of boxes')
        parser.add_option (
            '-p', '--picks', dest='picks', 
            default=50, type='int', help='number of picks')
        parser.add_option (
            '-v', '--verbose', action='store_true',
            default=False, help='verbose output')
        (options, args) = parser.parse_args()
        if options.verbose: print('START: ' + datetime.utcnow().isoformat())
        main()
        if options.verbose: print('STOP : ' + datetime.utcnow().isoformat())
        if options.verbose: print('TOTAL RUNNING TIME IN MINUTES: ' + str((time.time() - start_time) / 60.0))
        sys.exit(0)
    except KeyboardInterrupt as e: # Ctrl-C
        raise e
    except SystemExit as e: # sys.exit()
        raise e
    except Exception as e:
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(e))
        traceback.print_exc()
        os._exit(1)