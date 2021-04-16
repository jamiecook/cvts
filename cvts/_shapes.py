import numpy as np
from typing import Dict, Union, Tuple
import shapefile # intalled by pyshp
import shapely.geometry
from shapely.geometry import Polygon, MultiPolygon



status = print



def read_shapefile(
        filename: str,
        geometry_id_field: str) -> str:
    """Load the data from a shapefile.

    :param filename: The name of the shapefile.

    :param geometry_id_field: The field to extract from the shapefile. This
        should contain the identifier for the geometries.

    :return: The name of the file the data in the shapefile was saved to."""

    sf = shapefile.Reader(filename)
    fields = {k: v for v, k in enumerate([x[0] for x in sf.fields[1:]])}
    col = fields[geometry_id_field]

    # extract (code, shapely) key-value pairs as dictionary
    temp_shape = {}
    for shape, record in zip(sf.iterShapes(), sf.iterRecords()):
        if shape.__geo_interface__:
            key = int(record[col])
            s = shapely.geometry.shape(shape.__geo_interface__)
            temp_shape[key] = s

    return _shapedata(temp_shape)



def _check_and_fix_poly(poly):
    if not poly.is_valid:
        fixed_poly = poly.buffer(0)
        if not fixed_poly.is_valid:
            raise Exception('unfixable geom')
        return fixed_poly
    else:
        return poly



def _shapedata(shapes: Dict[str, Union[Polygon, MultiPolygon]]) -> Tuple:
    """Prepare shapes for intersecting with points..

    Multipolygons are split into polygons with repeated keys.

    :param shapes: Dictionary of shapes keyed by geometry ides describing the
        regions in the geography."""

    keys = []
    polys = []
    status("Expanding multipolygons")
    status("{} shapes to...".format(len(shapes)))
    for k, p in shapes.items():
        if isinstance(p, Polygon):
            keys.append(k)
            polys.append(_check_and_fix_poly(p))
        elif isinstance(p, MultiPolygon):
            for q in p:
                keys.append(k)
                polys.append(_check_and_fix_poly(q)) # split into single polys
    status("{} polys.".format(len(keys)))

    keys = np.array(keys).astype(int)
    boxes = np.array([s.bounds for s in polys]).astype(np.float32)

    return keys, polys, boxes
