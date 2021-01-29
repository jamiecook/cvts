[return to parent](../README.md)



## Contents

- **build.bat**: Batch script for building binaries associated with Valhalla on windows. See the
  windows setup described below for when to use it.

- **test.bat**: Example/test script for creating OSM tiles on windows.

- **vcpkg.bat**: Batch script for setting up [vcpkg](https://github.com/microsoft/vcpkg) See below
  for when to use it.



## Steps on windows

These instructions and, in particular, assoicated files are written assuming that the root folder
for this work is at *G:\CVTS*, which refer to as the "project root". If you move the folder to
somewhere else, you will need to modify the batch files in this folder to point to that direction.

- Create a conda environment

    ```
    conda create -n cvts python-3.7
    ```

    You can activate this with `conda activate cvts` and subsequently deactivate it with `conda deactivate`.

- Install visual studio 2019.

- Install [CMake](https://cmake.org).

- Go to the project root with `cd /D G:\CVTS` (create that directory first if it does not already exist).

- Clone the required repositories from *git bash*

    ```
    git clone https://github.com/microsoft/vcpkg.git
    git clone https://github.com/CVTS/cvts.git
    git clone --recurse-submodules https://github.com/CVTS/valhalla.git
    ```

- Bootstrap and 'install' vcpkg with `.\cvts\vcpkg.bat` (using *cmd*)

- Build valhalla with `.\cvts\build.bat`

- Test valhalla

    ```
    conda activate cvts
    `.\cvts\test.bat`
    conda deactivate
    ```
