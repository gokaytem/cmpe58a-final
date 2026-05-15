# Matio Installation Guide (Windows 64-bit, MSVC, CMake, zlib + HDF5)

This guide explains how to build and install **zlib (static)**, **HDF5 (static, with zlib)**, and **matio (with HDF5 + zlib)** on **64-bit Windows** using **CMake** and **Visual Studio**.

> Goal: produce MSVC-compatible `.lib` outputs and install them under a clean dependency prefix.

---

## 1) Prerequisites

Install the following:

- **Windows 10/11 (64-bit)**
- **Visual Studio 2019 or 2022** with:
  - Desktop development with C++
  - MSVC x64 toolset
  - CMake tools for C++ (recommended)
- **CMake** (GUI and/or CLI)
- **Git** (optional, if cloning sources)

Verify from *x64 Native Tools Command Prompt for VS*:

```bat
cmake --version
cl
```

---

## 2) Download Source Archives

Download and extract:

- **zlib**: https://zlib.net/
- **HDF5**: https://www.hdfgroup.org/downloads/hdf5/
- **matio**: https://github.com/tbeu/matio/releases

Keep source trees in `C:\src` (example below).

---

## 3) Recommended Directory Layout

Use a predictable structure:

```text
C:\src\zlib-1.3.1
C:\src\hdf5-1.14.6
C:\src\matio-1.5.30

C:\build\zlib-vs
C:\build\hdf5-vs
C:\build\matio-vs

C:\deps\zlib
C:\deps\hdf5
C:\deps\matio
```

This separates **source**, **build**, and **install** outputs.

---

## 4) Build zlib (Static)

### 4.1 CMake GUI Steps

1. Open **CMake GUI**.
2. **Where is the source code**: `C:/src/zlib-1.3.1`
3. **Where to build the binaries**: `C:/build/zlib-vs`
4. Click **Configure**:
   - Generator: `Visual Studio 16 2019` (or `Visual Studio 17 2022`)
   - Platform: `x64`
5. Set:
   - `CMAKE_INSTALL_PREFIX = C:/deps/zlib`
   - `BUILD_SHARED_LIBS = OFF`
6. Click **Configure** again (until no red entries remain), then **Generate**.
7. Open generated `zlib.sln`.
8. Select configuration **Release | x64**.
9. Build target **INSTALL**.

### 4.2 Equivalent Command-Line Steps

```bat
cmake -S C:\src\zlib-1.3.1 -B C:\build\zlib-vs ^
  -G "Visual Studio 16 2019" -A x64 ^
  -DCMAKE_INSTALL_PREFIX=C:\deps\zlib ^
  -DBUILD_SHARED_LIBS=OFF

cmake --build C:\build\zlib-vs --config Release
cmake --build C:\build\zlib-vs --config Release --target INSTALL
```

Expected outputs:

```text
C:\deps\zlib\include
C:\deps\zlib\lib\zlibstatic.lib
```

If your zlib build produces `zlib.lib` instead, use that exact filename consistently in later `ZLIB_LIBRARY` and linker settings.

---

## 5) Build HDF5 (Static, with zlib)

### 5.1 CMake GUI Steps

1. Open **CMake GUI**.
2. Source: `C:/src/hdf5-1.14.6`
3. Build: `C:/build/hdf5-vs`
4. **Configure** with Visual Studio x64 generator.
5. Set:
   - `CMAKE_INSTALL_PREFIX = C:/deps/hdf5`
   - `BUILD_SHARED_LIBS = OFF`
   - `HDF5_ENABLE_Z_LIB_SUPPORT = ON`
   - `ZLIB_ROOT = C:/deps/zlib`
6. Re-run **Configure** and then **Generate**.
7. Open generated `HDF5.sln`.
8. Build **Release | x64**.
9. Build target **INSTALL**.

### 5.2 Equivalent Command-Line Steps

```bat
cmake -S C:\src\hdf5-1.14.6 -B C:\build\hdf5-vs ^
  -G "Visual Studio 16 2019" -A x64 ^
  -DCMAKE_INSTALL_PREFIX=C:\deps\hdf5 ^
  -DBUILD_SHARED_LIBS=OFF ^
  -DHDF5_ENABLE_Z_LIB_SUPPORT=ON ^
  -DZLIB_ROOT=C:\deps\zlib

cmake --build C:\build\hdf5-vs --config Release
cmake --build C:\build\hdf5-vs --config Release --target INSTALL
```

Expected outputs:

```text
C:\deps\hdf5\include
C:\deps\hdf5\lib\hdf5.lib
C:\deps\hdf5\lib\hdf5_hl.lib
```

---

## 6) Build matio (with HDF5 + zlib)

### 6.1 CMake GUI Steps

1. Open **CMake GUI**.
2. Source: `C:/src/matio-1.5.30`
3. Build: `C:/build/matio-vs`
4. **Configure** with Visual Studio x64 generator.
5. Set:
   - `CMAKE_INSTALL_PREFIX = C:/deps/matio`
   - `MATIO_WITH_ZLIB = ON`
   - `MATIO_WITH_HDF5 = ON`
   - `MATIO_SHARED = OFF` (or `BUILD_SHARED_LIBS = OFF` if `MATIO_SHARED` is not present)
   - `ZLIB_INCLUDE_DIR = C:/deps/zlib/include`
   - `ZLIB_LIBRARY = C:/deps/zlib/lib/zlibstatic.lib`
   - `HDF5_DIR = C:/deps/hdf5/cmake/hdf5` (set this to the folder containing `HDF5Config.cmake`)
6. Re-run **Configure** until all dependency variables resolve.
7. Click **Generate**.
8. Open generated `matio.sln`.
9. Build **Release | x64**.
10. Build target **INSTALL**.

### 6.2 Equivalent Command-Line Steps

```bat
cmake -S C:\src\matio-1.5.30 -B C:\build\matio-vs ^
  -G "Visual Studio 16 2019" -A x64 ^
  -DCMAKE_INSTALL_PREFIX=C:\deps\matio ^
  -DMATIO_WITH_ZLIB=ON ^
  -DMATIO_WITH_HDF5=ON ^
  -DMATIO_SHARED=OFF ^
  -DZLIB_INCLUDE_DIR=C:\deps\zlib\include ^
  -DZLIB_LIBRARY=C:\deps\zlib\lib\zlibstatic.lib ^
  -DHDF5_DIR=C:\deps\hdf5\cmake\hdf5

cmake --build C:\build\matio-vs --config Release
cmake --build C:\build\matio-vs --config Release --target INSTALL
```

If CMake cannot locate HDF5, find `HDF5Config.cmake` and use its parent directory for `-DHDF5_DIR`:

```bat
dir /s /b C:\deps\hdf5\HDF5Config.cmake
```

Expected outputs:

```text
C:\deps\matio\include
C:\deps\matio\lib\matio.lib
```

---

## 7) Validation Steps

### 7.1 Verify Install Trees

Confirm all directories exist:

```text
C:\deps\zlib\include
C:\deps\zlib\lib
C:\deps\hdf5\include
C:\deps\hdf5\lib
C:\deps\matio\include
C:\deps\matio\lib
```

### 7.2 Minimal Consumer Check (CMake)

Create a minimal project (for example in `C:\tmp\matio-check`) and test link.

`CMakeLists.txt`:

```cmake
cmake_minimum_required(VERSION 3.20)
project(matio_check C)

add_executable(matio_check main.c)

target_include_directories(matio_check PRIVATE
  "C:/deps/matio/include"
  "C:/deps/hdf5/include"
  "C:/deps/zlib/include"
)

target_link_directories(matio_check PRIVATE
  "C:/deps/matio/lib"
  "C:/deps/hdf5/lib"
  "C:/deps/zlib/lib"
)

target_link_libraries(matio_check PRIVATE
  matio
  hdf5
  hdf5_hl
  zlibstatic
)
```

`main.c`:

```c
#include <matio.h>

int main(void) {
    mat_t *mat = Mat_CreateVer("check.mat", NULL, MAT_FT_MAT5);
    if (mat) {
        Mat_Close(mat);
    }
    return 0;
}
```

Build test app:

```bat
cmake -S C:\tmp\matio-check -B C:\tmp\matio-check\build ^
  -G "Visual Studio 16 2019" -A x64
cmake --build C:\tmp\matio-check\build --config Release
```

If build succeeds and `check.mat` is generated at runtime, your installation is working.

---

## 8) Troubleshooting

- **Cannot find HDF5**:
  - Set `HDF5_DIR` to the folder containing `HDF5Config.cmake`.
- **zlib library not found**:
  - Ensure `ZLIB_LIBRARY` points to the actual `.lib` produced by your zlib build.
- **Architecture mismatch errors**:
  - Make sure every build uses **x64** (zlib, HDF5, matio, and your app).
- **Debug/Release mismatch**:
  - Link Release libs with Release app, Debug libs with Debug app.
