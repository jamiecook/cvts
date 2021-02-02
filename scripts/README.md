[return to parent](../README.md)

# Scripts

## Contents

- **csv2json.py**: Python script for converting CSVs to JSON appropriate for feeding to the
  [trace_attributes](https://valhalla.readthedocs.io/en/latest/api/map-matching/api-reference/#outputs-of-trace_attributes)
  service of Valhalla.

- **json2geojson.py**: Python script for converting the json files produced by the
  [trace_attributes](https://valhalla.readthedocs.io/en/latest/api/map-matching/api-reference/#outputs-of-trace_attributes)
  service of Valhalla to GeoJSON files.

- **polyline.py**: Python module for for encoding and decoding linestrings using the Google encoded
  polyline algorithm. Copied from https://gist.github.com/signed0/2031157.
