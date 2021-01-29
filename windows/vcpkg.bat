set PROJECT_ROOT=G:\CVTS

cd %PROJECT_ROOT%\vcpkg
.\bootstrap-vcpkg.bat
vcpkg integrate install

cd %PROJECT_ROOT%
