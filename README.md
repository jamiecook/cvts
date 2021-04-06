# CVTS

Misc stuff related to the CVTS project.



## Contents

- **[bin](./bin/README.md)**: Python scripts used in this project.

- **convert.py**: Python script for making sure the example data is appropriately anonymised."""

- **cvts**: Python code used in this project, structured as a Python package.

- **setup.py**: Setup script for the python package.

- **test.csv**: A test 'track' (can be prepared with *bin/csv2json*).

- **test.json**: The example data contained in *test.csv* converted for input by
  *bin/csv2json*. This is only here for ease of reference.

- **test.sh**: A test script that downloads and prepares the data for Vietnam and runs an example
  CSV file against the
  [trace_attributes](https://valhalla.readthedocs.io/en/latest/api/map-matching/api-reference/#outputs-of-trace_attributes)
  service in 'one shot' mode. **Must be run in this folder.*

- **[windows](./windows/README.md)**: Stuff for setting up on windows...
  probably way out of date.



## Getting started

You will need to have [Valhalla](https://github.com/CVTS/valhalla) installed.
See [windows/README](./windows/README.md) for instructions for getting started
on windows. On Linux (Ubuntu)... just follow the instructions in [the README in
the Valhalla repo](https://github.com/CVTS/valhalla).

To setup this repo, you can install the python package with (using virtualenv):

```bash
# Clone this repository
git clone git@github.com:cvts/cvts.git

cd cvts

# make a virtual env
virtualenv -p python3 venv && . venv/bin/activate

# and install
pip install .

# get the Vietnam data and check that it is all working
./test.sh
```



## Useful Stuff

- Online documentation for Valhalla can be found
  [here](https://valhalla.readthedocs.io/en/latest/).



## Sharing a tmux Session

- Person who is going to host

  Ensure that the file */tmp/shareds* does not exist. If it does, change the
*/tmp/shared* it what follows to some other file.

    ```bash
    tmux -S /tmp/shareds new -s shared
    chgrp ACL_STACC_LW-CVTS_ADM /tmp/shareds
    ```

- Person who is guest

    ```bash
    tmux -S /tmp/shareds attach -t shared

    # or, read only
    tmux -S /tmp/shareds attach -t shared -r
    ```
