[return to parent](../README.md)

# Config

Various configuration files and stuff.

## Contents

- **files.pkl**: List of files for each truck. Produced by `processtraces` by
  walking the contents of *../raw*. It can take quite a while to gather these
  data, so we cache them. Delete this file if you want to regenerate the list of
  files, which you would do, for instance, if you have added more files.

- **valhalla.json**: Valhalla configuration. Would usually be produced by running
  *test.sh* in the root of the cvts repo.

- **valhalla\_tiles**: Valhalla tiles. Would usually be produced by running
  *test.sh* in the root of the cvts repo.

- **valhalla\_tiles.tar**: tar of *valhalla\_tiles*. Would usually be produced
  by running *test.sh* in the root of the cvts repo.

- **vietnam-latest.osm.pbf**: 'raw' OSM data. May be downloaded when running
  *test.sh* in the root of the cvts repo. However, we just symlink to a
  definitive version for now.
