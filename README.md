# CVTS

Misc stuff related to the CVTS project.

More complete documentation available [here](https://cvts.github.io/cvts/).



## Contents

- **bin**: Python scripts used in this project.

- **convert.py**: Python script for making sure the example data is
  appropriately anonymised."""

- **cvts**: Python code used in this project, structured as a Python package.

- **doc**: Sphinx documentation. Make this with `make sphinx-doc` (requires
  that you have run `make initial-setup` some time previously) and then access
  it at *doc/build/index.html*

- **setup.py**: Setup script for the python package.

- **test.csv**: A test 'track' (can be prepared with *bin/csv2json*).

- **test.json**: The example data contained in *test.csv* converted for input by
  *bin/csv2json*. This is only here for ease of reference.

- **test.sh**: A test script that downloads and prepares the data for Vietnam
  and runs an example CSV file against the
  [trace_attributes](https://valhalla.readthedocs.io/en/latest/api/map-matching/api-reference/#outputs-of-trace_attributes)
  service in 'one shot' mode. **Must be run in this folder.**

- **[windows](./windows/README.md)**: Stuff for setting up on windows...
  probably way out of date.



## Getting started

You will need to have [Valhalla](https://github.com/CVTS/valhalla) installed.
See [windows/README](./windows/README.md) for instructions for getting started
on windows. On Linux (Ubuntu)... just follow the instructions in [the README in
the Valhalla repo](https://github.com/CVTS/valhalla).


### Setup on Centos (from first setup of WB machine):

```bash
sudo yum group install -y "Development Tools"
sudo yum install -y \
    cmake3 \
    curl-devel \
    czmq-devel \
    minizip-devel \
    proj-devel \
    zeromq-devel \
    libxml2-devel \
    luajit-devel

    # boost-devel
    # protobuf-devel
    # sqlite-devel
    # geos-devel

# default curl does not work
# from https://serverfault.com/questions/321321/upgrade-curl-to-latest-on-centos
sudo echo "[CityFan]
name=City Fan Repo
baseurl=http://www.city-fan.org/ftp/contrib/yum-repo/rhel$releasever/$basearch/
enabled=1
gpgcheck=0" > /etc/yum.repos.d/city-fan.repo
sudo yum clean all
sudo install curl

# default gcc on Centos is too old (for Valahalla)
# from https://stackoverflow.com/questions/55345373/how-to-install-gcc-g-8-on-centos
sudo yum install centos-release-scl
sudo yum install devtoolset-8-gcc devtoolset-8-gcc-c++
scl enable devtoolset-8 -- bash

# install boost (packaged version has missing files... too old?)
cd ~
wget https://boostorg.jfrog.io/artifactory/main/release/1.66.0/source/boost_1_66_0.tar.gz
tar -xzf boost_1_66_0.tar.gz
cd boost_1_66_0
./bootstrap.sh
sudo ./b2 --with-program_options install

# install protobuf (packaged version too old)
cd ~
git clone --recurse-submodules https://github.com/protocolbuffers/protobuf.git
cd protobuf
./autogen.sh
./configure
make -j8 && sudo make install

# build and install sqlite (appears the latest on centos is too old)
cd ~
git clone https://github.com/sqlite/sqlite.git
cd sqlite
./configure --enable-rtree
make -j8 && sudo make install

# build and install geos
cd ~
git clone https://github.com/libgeos/geos.git
# remove the -Werror from CMakelists.txt (about line 243)
mkdir build
cd build
cmake3 -DCMAKE_BUILD_TYPE=Release ..
make && sudo make install

# build and install freexl # ???
cd ~
wget http://www.gaia-gis.it/gaia-sins/freexl-1.0.6.tar.gz
tar -xzf freexl-1.0.6.tar.gz
cd freexl-1.0.6
./configure
make && sudo make install

# build and install librttopo
cd ~
git clone https://git.osgeo.org/gitea/rttopo/librttopo.git
cd librttopo
./autogen.sh
./configure
make && sudo make install

# build and install readosm
cd ~
wget http://www.gaia-gis.it/gaia-sins/readosm-1.1.0a.tar.gz
tar -zxf readosm-1.1.0a.tar.gz
cd readosm-1.1.0a
./configure
make -j 8
sudo make install

# build and install spatiallite (packaged version too old)
cd ~
wget http://www.gaia-gis.it/gaia-sins/libspatialite-5.0.1.tar.gz
tar -xzf libspatialite-5.0.1.tar.gz
cd libspatialite-5.0.1
./configure --disable-knn
make && sudo make install

## build and install spatiallite-tools
## not sure if this is required in the end (disabling tests and benchmarks)
#cd ~
#wget http://www.gaia-gis.it/gaia-sins/spatialite-tools-5.0.0.tar.gz
#tar -xzf spatialite-tools-5.0.0.tar.gz
#cd spatialite-tools-5.0.0
#PKG_CONFIG_PATH=/usr/local/lib/pkgconfig ./configure
#make -j 8
#sudo make install

# don't think needed if we have -DENABLE_SERVICES=OFF in Valahalla
## install prime server
#cd ~
#git clone --recursive https://github.com/kevinkreiser/prime_server.git
#cd prime_server
#mkdir build && cd build
#cmake3 .. -DCMAKE_BUILD_TYPE=Release
#make -j8 && sudo make install

# ... and finally, valhalla itself
cd ~
git clone --recursive https://github.com/CVTS/valhalla.git
cd valhalla
mkdir build && cd build
cmake3 -DCMAKE_BUILD_TYPE=Release -DENABLE_SERVICES=OFF -DENABLE_TESTS=OFF -DENABLE_BENCHMARKS=OFF ..
make -j8 && sudo make install
```


### In General

```bash
# Clone this repository
git clone git@github.com:cvts/cvts.git && cd cvts

# make a virtual env
make setup-venv && . venv/bin/activate

# and install
pip install .

# get the Vietnam data and check that it is all working
./test.sh

# You deactivate the virtual env with
deactivate
```


Alternatively, for development in particular, you might say

```bash
make initial-setup
. venv/bin/activate
./test.sh
deactivate
```



## Config

Configuration is controlled by *cvts/settings.py*. This expects the environment
variable *CVTS_WORK_PATH* to be set, which specifies the root folder for input/output
data. One can optionally set specify the the following environment variables

- *CVTS_BOUNDARIES_PATH*: The directory in regional shape files are stored,

- *CVTS_RAW_PATH*: The directory in which the raw data is stored,

- *CVTS_CONFIG_PATH*: The directory in which the configuration data is stored
  (see the [documentation for the config directory](doc/README-config-folder.md
  for details), and

- *CVTS_OUT_PATH*: The directory where outputs will be saved.
