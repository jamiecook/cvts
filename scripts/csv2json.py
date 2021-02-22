#!/usr/bin/env python

#------------------------------------------------------------------------------
# Script for converting a (Vietnam) CSV to a JSON file suitable for feeding to
# valhalla_service <config.json> trace_attributes.
#
# Takes upto two arguments:
# 1. The name of the input file (compulsory),
# 2. The name of an output file (optional), and
# 3. 0 or 1 (default is 1), which is converted to a boolean. Determines if the
#    input locations should be reversed. Adam found that reversing gave much
#    better results, but we were not sure why.
#
# If the second argument is not provided, the path to the output file will be
# the path to the input file with the extension changed to 'json'.
#------------------------------------------------------------------------------

import os
import sys
import csv
import json

def convert(infile, outfile, reverse=True):
    with open(infile, 'r') as cf:
        reader = csv.DictReader(cf)
        locs = [{
                'lat': float(row['Longitude']),
                'lon': float(row['Latitude']),
                'time': float(row['Time']),
                'heading': float(row['Orientation']),
                'heading_tolerance': 45,
                'type': 'via'} for i, row in enumerate(reader)]

        locs.sort(key=lambda i: i['time'], reverse=reverse)

        lls = {
            'shape': locs,
            'costing': 'auto',
            'shape_match': 'map_snap'}

        lls['shape'][0]['type'] = 'break'
        lls['shape'][-1]['type'] = 'break'

        with open(outfile, 'w') as jf:
            json.dump(lls, jf, indent=4)

if __name__ == '__main__':
    inputfile = sys.argv[1]
    outputfile = sys.argv[2] if len(sys.argv) > 2 else (os.path.splitext(inputfile)[0] + '.json')
    reverse = bool(sys.argv[3]) if len(sys.argv) > 3 else True
    convert(inputfile, outputfile, reverse)
