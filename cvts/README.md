[return to parent](../README.md)

Python code used in the CVTS project, structured as a Python package.

- **__init__.py**: Contains most of the code specific to this work.

- **_interesect.py**: Perform an intersection between a set of points and a set
  of polygons.  This was ripped out of YDYR and original written by Alistair
  Reid.

- **_polyline.py**: Python module for for encoding and decoding linestrings
  using the Google encoded polyline algorithm. Copied from
  https://gist.github.com/signed0/2031157.

- **_shapes.py**: Tool for loading data from a shape file which is suitable to
  us with the tools in *_intersect.py.py*.

- **settings.py**: Settings. Things like the location of where to
  find/read/write files.
