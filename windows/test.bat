rem This is based on the instructions found in the README.md of the valhalla repo.

set PROJECT_ROOT=G:\CVTS

set TEST_ROOT=%PROJECT_ROOT%\test
set VALHALLA_DIR=%PROJECT_ROOT%\valhalla
set SCRIPTS_DIR=%VALHALLA_DIR%\scripts
set BUILD_TILES=%VALHALLA_DIR%\build\Debug\valhalla_build_tiles

mkdir %TEST_ROOT%
cd %TEST_ROOT%

rem download some data
rem NOTE: THIS TAKES A FAIR WHILE TO EXECUTE
curl -o switzerland-latest.osm.pbf http://download.geofabrik.de/europe/switzerland-latest.osm.pbf
curl -o liechtenstein-latest.osm.pbf http://download.geofabrik.de/europe/liechtenstein-latest.osm.pbf

rem get the config and setup
mkdir valhalla_tiles
python %SCRIPTS_DIR%\valhalla_build_config^
    --mjolnir-tile-dir %TEST_ROOT%/valhalla_tiles^
    --mjolnir-tile-extract %TEST_ROOT%/valhalla_tiles.tar^
    --mjolnir-timezone %TEST_ROOT%/valhalla_tiles/timezones.sqlite^
    --mjolnir-admin %TEST_ROOT%/valhalla_tiles/admins.sqlite > valhalla.json

rem build routing tiles
%BUILD_TILES% -c valhalla.json switzerland-latest.osm.pbf liechtenstein-latest.osm.pbf



cd %PROJECT_ROOT%
rem not sure how to do the stuff below here on windows.



rem rem tar it up for running the server
rem find valhalla_tiles | sort -n | tar cf valhalla_tiles.tar --no-recursion -T -

rem rem grab the demos repo and open up the point and click routing sample
rem git clone --depth=1 --recurse-submodules --single-branch --branch=gh-pages https://github.com/valhalla/demos.git
rem firefox demos/routing/index-internal.html &
rem rem NOTE: set the environment pulldown to 'localhost' to point it at your own server

rem rem start up the server
rem valhalla_service valhalla.json 1
rem rem curl it directly if you like:
rem curl http://localhost:8002/route --data '{"locations":[{"lat":47.365109,"lon":8.546824,"type":"break","city":"Zürich","state":"Altstadt"},{"lat":47.108878,"lon":8.394801,"type":"break","city":"6037 Root","state":"Untere Waldstrasse"}],"costing":"auto","directions_options":{"units":"miles"}}' | jq '.'
