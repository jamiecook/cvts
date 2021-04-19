import csv
import json
from math import sqrt, radians, cos
from functools import reduce
from ._polyline import decode
from ._intersect import points_to_polys
from ._shapes import read_shapefile



MAGIC_TIME     = 20 * 60 # s
MAGIC_SPEED    = 6       # km/h
MAGIC_DISTANCE = 50      # m
EARTH_RADIUS   = 6371000 # m



def distance(x0, y0, x1, y1):
    # quick and adequate for small distances
    yd = radians(y1 - y0)
    xd = radians(x1 - x0) * cos(radians(y0) + .5*yd)
    return EARTH_RADIUS * sqrt(yd*yd + xd*xd)



def _trip_slices(locs):
    if len(locs) == 0:
        yield slice(0, 0)

    else:
        getter = lambda l: (l['time'], l['speed'], l['lat'], l['lon'])
        zi = enumerate(getter(l) for l in locs)
        has_moved = False
        li, (last_moved_time, _, ly, lx) = next(zi)
        last_point_time = last_moved_time
        i = li

        for i, (t, s, y, x) in zi:
            has_moved = has_moved or distance(lx, ly, x, y) > MAGIC_DISTANCE or s > MAGIC_SPEED

            if has_moved:
                if t - last_moved_time > MAGIC_TIME:
                    if t - last_point_time <= MAGIC_TIME:
                        yield slice(li, i-1)
                        li = i-1
                    else:
                        yield slice(li, i)
                        li = i
                    has_moved = False
                lx, ly, last_moved_time = x, y, t

            last_point_time = t

        yield slice(li, i+1)



def _loadcsv(csvfile):
    with open(csvfile, 'r') as cf:
        reader = csv.DictReader(cf)
        return [{
            'lat': float(row['Longitude']),
            'lon': float(row['Latitude']),
            'time': float(row['Time']),
            'heading': float(row['Orientation']),
            'speed': float(row['speed']),
            'heading_tolerance': 45,
            'type': 'via'} for row in reader]



def _prepjson(locs, split_time):
    locs.sort(key=lambda l: l['time'])
    if split_time:
        for split in _trip_slices(locs):
            locs = locs[split]
            if len(locs) == 0:
                continue
            locs[0]['type'] = 'break'
            locs[-1]['type'] = 'break'
            yield {'shape': locs, 'costing': 'auto', 'shape_match': 'map_snap'}
    else:
        locs[0]['type'] = 'break'
        locs[-1]['type'] = 'break'
        yield {'shape': locs, 'costing': 'auto', 'shape_match': 'map_snap'}



def csvfiles2jsonchunks(csvfile, split_time):
    raw_locs = _loadcsv(csvfile) \
        if isinstance(csvfile, str) \
        else reduce(lambda a, b: a + _loadcsv(b), csvfile, [])
    return _prepjson(raw_locs, split_time)

def csvfiles2jsonfile(csvfile, outfile):
    chunks = csvfiles2jsonchunks(csvfile, False)
    with open(outfile, 'w') as jf:
        json.dump(next(chunks), jf, indent=4)



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
