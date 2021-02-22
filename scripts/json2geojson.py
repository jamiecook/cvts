#!/usr/bin/env python

#------------------------------------------------------------------------------
# Script for converting a (Vietnam) JSON produced by trace_attributes to
# GeoJSON.
#
# Takes upto two arguments:
# 1. The name of the input file (compulsory), and
# 2. The name of an output file (optional)
#
# If the second argument is not provided, the path to the output file will be
# the path to the input file with the extension changed to 'geojson'.
#------------------------------------------------------------------------------

import os
import sys
import json
from polyline import decode

def point_feature(matched_point):
    lat = matched_point.pop('lat')
    lon = matched_point.pop('lon')
    return {
        'type': 'Feature',
        'properties': matched_point,
        'geometry': {
            'type': 'Point',
            'coordinates': [lon, lat]}}

def convert(infile, outfile):
    with open(infile, 'r') as jf:
        # the matched points
        data = json.load(jf)
        shape = [{
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': [[p[0]/10., p[1]/10.] for p in decode(data['shape'])]}}]

        gj = {
            'type': 'FeatureCollection',
            'features': [point_feature(mp) for mp in data['matched_points']] + shape}

        with open(outfile, 'w') as gf:
            json.dump(gj, gf, indent=4)

        # the path
        gj = {
            'type': 'FeatureCollection',
            'features': shape}

        with open(os.path.splitext(outfile)[0] + '-shape.geojson', 'w') as gf:
            json.dump(gj, gf, indent=4)

if __name__ == '__main__':
    inputfile = sys.argv[1]
    outputfile = sys.argv[2] if len(sys.argv) > 2 else (os.path.splitext(inputfile)[0] + '.geojson')
    convert(inputfile, outputfile)
