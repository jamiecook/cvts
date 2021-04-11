[return to parent](../README.md)

# Outputs

Outputs produced by the program `processtraces`.

## Contents

- **mm**: CSVs for each vehicle. An example of the contents of each CSV is

```
lat,lon,time,heading,speed,heading_tolerance,status,trip_index,way_id,valhalla_speed,speed_limit,message
10.862250328064,106.928115844727,1501545600.0,180.0,0.0,45,success,0,829395784,20,NA,matched
10.8622531890869,106.928123474121,1501545727.0,180.0,0.0,45,success,0,829395784,20,NA,interpolated
10.8622550964355,106.928123474121,1501546327.0,180.0,0.0,45,success,0,829395784,20,NA,interpolated
...
```

Each row corresponds to an input point, and all input points are included.
**Note that the order of the points may not correspond to the order of points
in the input files.**

    The fields are:

    - *lat*: The latitude of the point (from the GPS trace).

    - *lon*: The longitude of the point (from the GPS trace).

    - *time*: The timestamp of the point (from the GPS trace).

    - *speed*: The speed at the point (from the GPS trace).

    - *heading*: The heading at the point (from the GPS trace).

    - *heading_tolerance*: The heading tolerance specified for the point. This is
      specified by our software and used internally by Valhalla for calculating
      costs when doing the matching.

    - *status*: One of "success" or "failure", denoting whether matching succeeded
      or failed for the point.

    - *trip_index*: The index of the trip, which is just a counter (starting at zero)
      which is indexed for every trip. This is produced by our code.

    - *way_id*: The identifier of the way Valhalla matched the point to.

    - *valhalla_speed*: The speed reported by Valhalla.

    - *speed_limit*: The speed limit on the way reported by Valhalla.

    - *message*: Either the match type returned by Valhalla, or an error message
      (the result of `str(e)`, where `e` is the exception thrown in the case where
      *status* is "failure".



- **seq**: JSON data for each vehicle. The JSON data contains a list of dicts,
  one for each trip. Each dict contains:

    - "status": "success" if Valhalla succeeded for this trip or "failure" if
      it did not.
    - "trip\_index": The index of the trip.
    - "start":
        - "time": The timestamp of the point at which the trip started.
        - "loc":
            - "lat": The latitude of the point at which the trip started.
            - "lon": The longitude of the point at which the trip started.
    - ["way\_ids"]: The way ids of the trip as produced by Valhalla. Only
      present if *status* is "success"
    - ["message"]: An error message. The result of `str(e)`, where `e` is the
      exception thrown in the case where *status* is "failure". Only present
      when *status* is "failure".
