#!/bin/bash

#------------------------------------------------------------------------------
# Script for installing data for Vietnam and running a test 'snap'.
#------------------------------------------------------------------------------

# get data for Vietnam
mkdir -p test
cd test
wget https://download.geofabrik.de/asia/vietnam-latest.osm.pbf

#get the config and setup
mkdir -p valhalla_tiles
valhalla_build_config \
    --mjolnir-tile-dir ${PWD}/valhalla_tiles \
    --mjolnir-tile-extract ${PWD}/valhalla_tiles.tar \
    --mjolnir-timezone ${PWD}/valhalla_tiles/timezones.sqlite \
    --mjolnir-admin ${PWD}/valhalla_tiles/admins.sqlite > valhalla.json

#build routing tiles
valhalla_build_tiles -c valhalla.json vietnam-latest.osm.pbf

#tar it up for running the server
find valhalla_tiles | sort -n | tar cf valhalla_tiles.tar --no-recursion -T -

# convert the test CSV data to JSON
../csv2json.py ../test.csv test.json

# and produce some output
valhalla_service valhalla.json trace_attributes test.json > snap.json
