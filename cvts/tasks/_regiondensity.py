#!/usr/bin/env python3

import os
import json
import pickle
from multiprocessing import Pool
from functools import partial
from datetime import timezone, timedelta
from math import floor, ceil
import numpy as np
from tqdm import tqdm
import luigi
from .. import (
    read_shapefile,
    points_to_polys,
    distance)
from ..settings import (
    OUT_PATH,
    STOP_PATH,
    SRC_DEST_PATH,
    BOUNDARIES_PATH)
from ._valhalla import MatchToNetwork



DEFAULT_BOUNDARIES = 'District'
GEOM_ID_COLUMN     = {'District': 'DistrictID', 'trans_cities': 'OBJECTID'}
MAGIC_DISTANCE     = 50 # m
TZ                 = timezone(timedelta(hours=7), 'ITC')

MINLAT   =   7.8584
MAXLAT   =  23.8882
MINLON   = 101.9988
MAXLON   = 109.3325
CELLSIZE =   0.1
NA_VALUE = -9999

STOP_POINTS_LAT_LON_FILE             = 'stop_points_lat_lon.pkl'
STOP_POINTS_GEOM_IDS_FILE            = 'stop_points_geom_ids.pkl'
STOP_POINTS_GEOM_COUNTS_FILE         = 'stop_points_geom_counts.pkl'
STOP_POINTS_GEOM_COUNTS_CSV_FILE     = 'stop_points_geom_counts.csv'

SRC_DEST_POINTS_LAT_LON_FILE         = 'src_dest_points_lat_lon.pkl'
SRC_DEST_POINTS_GEOM_IDS_FILE        = 'src_dest_points_geom_ids.pkl'
SRC_DEST_POINTS_GEOM_COUNTS_FILE     = 'src_dest_points_geom_counts.pkl'
SRC_DEST_POINTS_GEOM_COUNTS_CSV_FILE = 'src_dest_points_geom_counts.csv'



class Grid:
    """Raster used for accumulating stop points."""

    def __init__(
            self,
            minlat   = MINLAT,
            minlon   = MINLON,
            maxlat   = MAXLAT,
            maxlon   = MAXLON,
            cellsize = CELLSIZE,
            na_value = NA_VALUE):
        self.minlat = minlat
        self.minlon = minlon
        self.cellsize = cellsize
        self.na_value = na_value
        self.ncol = int(ceil((maxlon - self.minlon) / self.cellsize))
        self.nrow = int(ceil((maxlat - self.minlat) / self.cellsize))
        self.cells = np.zeros((self.nrow, self.ncol), int)

    def increment(self, lon, lat):
        row = self.nrow - int(floor((lon - self.minlon) / self.cellsize)) - 1
        col =             int(floor((lat - self.minlat) / self.cellsize))
        if 0 <= col < self.ncol and 0 <= row < self.nrow:
            self.cells[row, col] += 1
        # TODO: warning here?

    def save(self, fn):
        with open(fn, 'w') as f:
            f.write('ncols        {}\n'.format(self.ncol))
            f.write('nrows        {}\n'.format(self.nrow))
            f.write('xllcorner    {}\n'.format(self.minlon))
            f.write('yllcorner    {}\n'.format(self.minlat))
            f.write('cellsize     {}\n'.format(self.cellsize))
            f.write('NODATA_value {}\n'.format(self.na_value))
            f.write(' '.join([str(i) for i in self.cells.flatten()]))



def _ends(end, start):
    """Generator over stop points at the intersection of two trips.

    Given trips, use just one point if the end of the first trip is close enough
    to the beginning of the next trip, otherwise, use both the end of the first
    trip and the start of the second trip.

    Not sure why we would ever see the start of the second trip not be at the
    same location as the end of the first trip; my guess this implies some sort
    of missing data."""

    x1, y1 = start['lon'], start['lat']
    x0, y0 =   end['lon'],     end['lat']
    d = distance(x0, y0, x1, y1)
    yield x0, y0
    if d > MAGIC_DISTANCE:
        yield x1, y1

def _do_stops(filename):
    """Generator over the stop points for a trip.

    See :py:func:`_ends` for how the end/start of successive trips is handled."""

    rego = os.path.splitext(os.path.basename(filename))[0]

    with open(filename) as fin:
        stops = json.load(fin)

    stopiter = iter(stops)
    t0 = next(stopiter)
    p0 = t0['start']['loc']
    yield p0['lon'], p0['lat']
    for t1 in stopiter:
        for e in _ends(t0['end']['loc'], t1['start']['loc']):
            yield e
        t0 = t1
    p0 = t0['start']['loc']
    p1 = t0['end']['loc']
    if distance(p0['lon'], p0['lat'], p1['lon'], p1['lat']) > MAGIC_DISTANCE:
        yield p1['lon'], p1['lat']

def _do_source_dest(filename):
    """Generator over the source/dest points for a trip."""

    with open(filename) as fin:
        trips = json.load(fin)

    for trip in trips:
        loc = trip['start']['loc']
        yield loc['lon'], loc['lat']
        loc = trip['end']['loc']
        yield loc['lon'], loc['lat']

def _trip_iter(doer, out_path, filename):
    """Iterates over all trips for a vehicle."""

    out = [t for t in doer(filename)]
    out_file_name = os.path.join(out_path, os.path.basename(filename))
    with open(out_file_name, 'w') as out_file:
        json.dump(out, out_file)
    return np.array(out)

_stops = partial(_trip_iter, _do_stops, STOP_PATH)
_source_dests = partial(_trip_iter, _do_source_dest, SRC_DEST_PATH)



def _name_to_name_with_geom(name, geog_name, out_dir=OUT_PATH):
    rego, ext = os.path.splitext(name)
    return os.path.join(
        out_dir,
        '{}_{}{}'.format(rego, geog_name, ext))

#-------------------------------------------------------------------------------
# Luigi tasks
#-------------------------------------------------------------------------------
class _LocationPoints(luigi.Task):
    """Collects points for all trips of all vehicles."""

    pickle_file_basename = luigi.Parameter()
    point_extractor      = luigi.Parameter()

    @property
    def pickle_file_name(self):
        return os.path.join(OUT_PATH, self.pickle_file_basename)

    def requires(self):
        return MatchToNetwork()

    def run(self):
        with open(self.input()['seq'].fn, 'rb') as seq_files_file:
            all_seq_files = pickle.load(seq_files_file)

        with Pool() as p:
            workers = p.imap_unordered(self.point_extractor, all_seq_files)
            pnts = tqdm(workers, total=len(all_seq_files))
            stop_points = np.vstack([p for p in pnts if len(p) > 0])

        with open(self.output().fn, 'wb') as of:
            pickle.dump(stop_points, of)

    def output(self):
        return luigi.LocalTarget(self.pickle_file_name)



class _PointsToRegions(luigi.Task):
    """Maps the points to polygons in a region."""

    point_extractor            = luigi.Parameter()
    geometries_name            = luigi.Parameter()
    input_pickle_file_basename = luigi.Parameter()
    pickle_file_basename       = luigi.Parameter()

    @property
    def pickle_file_name(self):
        return _name_to_name_with_geom(
            self.pickle_file_basename,
            self.geometries_name)

    def requires(self):
        return _LocationPoints(
            self.input_pickle_file_basename,
            self.point_extractor)

    def run(self):
        # load the geometries
        polys = read_shapefile(
            os.path.join(BOUNDARIES_PATH, self.geometries_name + '.shp'),
            GEOM_ID_COLUMN[self.geometries_name])

        # load the stop points
        with open(self.input().fn, 'rb') as inf:
            stop_points = pickle.load(inf)

        # map the points to the polygons and save
        poly_points = points_to_polys(stop_points, polys)
        with open(self.output().fn, 'wb') as of:
            pickle.dump(poly_points, of)

    def output(self):
        return luigi.LocalTarget(self.pickle_file_name)



class _CountsTask(luigi.Task):
    geometries_name  = luigi.Parameter(default=DEFAULT_BOUNDARIES)

    @property
    def pickle_file_name(self):
        return _name_to_name_with_geom(
            self.pickle_file_basename,
            self.geometries_name)

    @property
    def csv_file_name(self):
        return _name_to_name_with_geom(
            self.csv_file_basename,
            self.geometries_name)

    def output(self):
        return luigi.LocalTarget(self.pickle_file_name)



class RegionCounts(_CountsTask):
    """Counts the number of stop points in each region."""

    pickle_file_basename = STOP_POINTS_GEOM_COUNTS_FILE
    csv_file_basename    = STOP_POINTS_GEOM_COUNTS_CSV_FILE

    def requires(self):
        return _PointsToRegions(
            _stops,
            self.geometries_name,
            STOP_POINTS_LAT_LON_FILE,
            STOP_POINTS_GEOM_IDS_FILE)

    def run(self):
        # get the counts in each region
        with open(self.input().fn, 'rb') as pf:
            poly_points = pickle.load(pf)
            vcs = np.unique(poly_points, return_counts=True)

        # write them to a pickle
        with open(self.output().fn, 'wb') as of:
            pickle.dump(vcs, of)

        # and write them to a CSV
        with open(self.csv_file_name, 'w') as of:
            of.write('{},count\n'.format('geom_id'))
            for vc in zip(*vcs):
                of.write('{},{}\n'.format(*vc))



class SourceDestinationCounts(_CountsTask):
    """Counts the number of stop points in each region."""

    pickle_file_basename = SRC_DEST_POINTS_GEOM_COUNTS_FILE
    csv_file_basename    = SRC_DEST_POINTS_GEOM_COUNTS_CSV_FILE

    def requires(self):
        return _PointsToRegions(
            _source_dests,
            self.geometries_name,
            SRC_DEST_POINTS_LAT_LON_FILE,
            SRC_DEST_POINTS_GEOM_IDS_FILE)

    def run(self):
        # get the counts in each region
        with open(self.input().fn, 'rb') as pf:
            gids  = pickle.load(pf)

            froms = gids[0::2]
            tos   = gids[1::2]

            ids   = np.array(['{}-{}'.format(*ft) for ft in zip(froms, tos)])
            _, indices, counts = np.unique(
                ids,
                return_index  = True,
                return_counts = True)

            froms = froms[indices]
            tos   =   tos[indices]

        # write them to a pickle
        with open(self.output().fn, 'wb') as of:
            pickle.dump((froms, tos, counts), of)

        # and write them to a CSV
        with open(self.csv_file_name, 'w') as of:
            of.write('from,to,count\n')
            for trip in zip(froms, tos, counts):
                of.write('{},{},{}\n'.format(*trip))



class RasterCounts(luigi.Task):
    """Counts the number of stop points in each cell of a raster."""

    ascii_grid_file_name = os.path.join(OUT_PATH, 'grid_points.asc')

    def requires(self):
        return _LocationPoints(STOP_POINTS_LAT_LON_FILE, _stops)

    def run(self):
        # load the stop points
        with open(self.input().fn, 'rb') as inf:
            stop_points = pickle.load(inf)

        # construct and save the grid counts
        grid = Grid()
        for p in stop_points:
            grid.increment(*p)
        grid.save(self.output().fn)

    def output(self):
        return luigi.LocalTarget(self.ascii_grid_file_name)
