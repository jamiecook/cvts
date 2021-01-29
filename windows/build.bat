set PROJECT_ROOT=G:\CVTS
set CMAKE="C:\Program Files\CMake\bin\cmake.EXE"

set VALHALLA_ROOT=%PROJECT_ROOT%\valhalla
set VALHALLA_BUILD=%VALHALLA_ROOT%\build

cd %VALHALLA_ROOT%
%PROJECT_ROOT%\vcpkg\vcpkg install --triplet x64-windows "@.vcpkg_deps.txt"`

mkdir %VALHALLA_BUILD%

%CMAKE% ^
    --no-warn-unused-cli ^
    -DENABLE_TOOLS=ON ^
    -DENABLE_DATA_TOOLS=ON ^
    -DENABLE_PYTHON_BINDINGS=ON ^
    -DENABLE_HTTP=ON ^
    -DENABLE_CCACHE=OFF ^
    -DENABLE_SERVICES=OFF ^
    -DENABLE_BENCHMARKS=OFF ^
    -DENABLE_TESTS=OFF ^
    -DLUA_LIBRARIES=%PROJECT_ROOT%\vcpkg\installed\x64-windows\lib\lua51.lib ^
    -DLUA_INCLUDE_DIR=%PROJECT_ROOT%\vcpkg\installed\x64-windows\include\luajit ^
    -DVCPKG_TARGET_TRIPLET=x64-windows ^
    -DCMAKE_TOOLCHAIN_FILE=%PROJECT_ROOT%\vcpkg\scripts\buildsystems\vcpkg.cmake ^
    -DCMAKE_EXPORT_COMPILE_COMMANDS:BOOL=TRUE ^
    -H%VALHALLA_ROOT% -B%VALHALLA_BUILD% ^
    -G "Visual Studio 16 2019" ^
    -T host=x64 -A x64

cd %PROJECT_ROOT%
