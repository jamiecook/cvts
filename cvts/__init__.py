import os
import csv
import json
from .polyline import decode



def csv2json(csvfile, reverse):
    with open(csvfile, 'r') as cf:
        reader = csv.DictReader(cf)
        locs = [{
                'lat': float(row['Longitude']),
                'lon': float(row['Latitude']),
                'time': float(row['Time']),
                'heading': float(row['Orientation']),
                'heading_tolerance': 45,
                'input_index': i,
                'type': 'via'} for i, row in enumerate(reader)]

        locs.sort(key=lambda l: l['time'], reverse=reverse)

        lls = {
            'shape': locs,
            'costing': 'auto',
            'shape_match': 'map_snap'}

        lls['shape'][0]['type'] = 'break'
        lls['shape'][-1]['type'] = 'break'

        return lls

def csvfile2jsonfile(csvfile, outfile, reverse=True):
    with open(outfile, 'w') as jf:
        locs = csv2json(csvfile, reverse)
        inds = [l['input_index'] for l in locs['shape']]
        json.dump(locs, jf, indent=4)
        return inds







def json2geojson(data):
    edges = data['edges']

    def _point_feature(matched_point, index):
        lat = matched_point.pop('lat')
        lon = matched_point.pop('lon')

        edge_index = matched_point.get('edge_index')
        matched_point['point_index'] = index
        if edge_index is not None:
            names = ', '.join(edges[edge_index].get("names", ["NA"]))
            matched_point['osname'] = names
            matched_point['way_id'] = edges[edge_index].get("way_id", "NA")

        return {
            'type': 'Feature',
            'properties': matched_point,
            'geometry': {
                'type': 'Point',
                'coordinates': [lon, lat]}}

    shape = [{
        'type': 'Feature',
        'geometry': {
            'type': 'LineString',
            'coordinates': [[p[0]/10., p[1]/10.] for p in decode(data['shape'])]}}]

    return {
        'type': 'FeatureCollection',
        'features': [_point_feature(mp, i) for i, mp in enumerate(data['matched_points'])] + shape}

def jsonfile2geojsonfile(infile, outfile):
    with open(infile, 'r') as jf, open(outfile, 'w') as gf:
        json.dump(json2geojson(json.load(jf)), gf, indent=4)
