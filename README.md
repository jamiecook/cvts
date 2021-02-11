# CVTS

Misc stuff related to the CVTS project.



## Contents

- **test.csv**: A test 'track' (can be prepared with *csv2json.py*).

- **test.sh**: A test script that downloads and prepares the data for Vietnam and runs an example
  CSV file against the
  [trace_attributes](https://valhalla.readthedocs.io/en/latest/api/map-matching/api-reference/#outputs-of-trace_attributes)
  service in 'one shot' mode.

- **[scripts](./scripts/README.md)**: Scripts and code.

- **[windows](./windows/README.md)**: Stuff for setting up on windows.



## Useful Stuff

- Online documentation for Valhalla can be found [here](https://valhalla.readthedocs.io/en/latest/).



## Setup

- Clone this repository

    ```bash
    git clone git@github.com:cvts/cvts.git
    ```

See [windows/README](./windows/README.md) for instructions for getting started on windows. On Linux
(Ubuntu)... just follow the instructions in
[the README in the Valhalla repo](https://github.com/CVTS/valhalla), and don't forget to look at
[this](https://github.com/CVTS/valhalla/blob/master/scripts/Ubuntu_Bionic_Install.sh).



## Testing

You can

- download data for Vietnam,

- built tiles, and

- run the data in *./test.csv* through the *trace\_attributes* 'one shot services

 with

```bash
./test.sh
```

This will all be done the folder *./test* (which will be created when you run *test.sh*).
