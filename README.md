# CVTS

Misc stuff related to the CVTS project.



## Contents

- **csv2json.py**: Python script for converting CSVs to JSON appropriate for feeding to the
  [trace_attributes](https://valhalla.readthedocs.io/en/latest/api/map-matching/api-reference/#outputs-of-trace_attributes)
  service of Valhalla.

- **test.csv**: A test 'track' (can be prepared with *csv2json.py*).

- **test.sh**: A test script that downloads and prepares the data for Vietnam and runs an example
  CSV file against the
  [trace_attributes](https://valhalla.readthedocs.io/en/latest/api/map-matching/api-reference/#outputs-of-trace_attributes)
  service in 'one shot' mode.

- **[windows](./windows/README.md)**: Stuff for setting up on windows.



## Useful Stuff

- Online documentation for Valhalla can be found [here](https://valhalla.readthedocs.io/en/latest/).



## Setup

See [windows/README](./windows/README.md) for instructions for getting started on windows. On Linux
(Ubuntu)... just follow the instructions in
[the README in the Valhalla repo](https://github.com/CVTS/valhalla), and don't forget to look at
[this](https://github.com/CVTS/valhalla/blob/master/scripts/Ubuntu_Bionic_Install.sh).
