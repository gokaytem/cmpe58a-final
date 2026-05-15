# Build and Install matio on 64-bit Windows (MSVC + CMake) with zlib and HDF5

This guide explains how to build **zlib**, **HDF5**, and **matio** on **64-bit Windows** using **CMake** and **Visual Studio** (MSVC), then validate the installation.

## 1) Prerequisites

- Windows 10/11 (64-bit)
- Visual Studio 2019 or newer with **Desktop development with C++** workload
- CMake (GUI and/or CLI)
- Git (optional but recommended for cloning sources)

### Verify tools from `x64 Native Tools Command Prompt`

```bat
cl
cmake --version
git --version
```

> Use an **x64** developer prompt to avoid mixing 32-bit and 64-bit toolchains.

## 2) Recommended folder layout

Use a clean directory structure (adjust paths as needed):

```text
C:\dev\src\zlib
C:\dev\src\hdf5
C:\dev\src\matio

C:\dev\build\zlib-vs
C:\dev\build\hdf5-vs
C:\dev\build\matio-vs

C:\dev\install\zlib
C:\dev\install\hdf5
C:\dev\install\matio
```

## 3) Download source code

You can use either release archives or Git clones.

### Option A: Git clone

```bat
git clone https://github.com/madler/zlib.git C:\dev\src\zlib
git clone https://github.com/HDFGroup/hdf5.git C:\dev\src\hdf5
git clone https://github.com/tbeu/matio.git C:\dev\src\matio
```

### Option B: Release ZIP/TAR

Download and extract each project into the `C:\dev\src\...` folders.

## 4) Build zlib (first dependency)

Build zlib first so HDF5 and matio can link against it.

---

### 4.1 CMake GUI method (zlib)

1. Open **CMake GUI**.
2. **Where is the source code**: `C:/dev/src/zlib`
3. **Where to build the binaries**: `C:/dev/build/zlib-vs`
4. Click **Configure**:
   - Generator: `Visual Studio 16 2019` (or installed VS generator)
   - Platform: `x64`
5. Set:
   - `CMAKE_INSTALL_PREFIX = C:/dev/install/zlib`
   - `BUILD_SHARED_LIBS = OFF` (static) **or** `ON` (shared)
6. Click **Generate**.
7. Open generated solution and build `INSTALL` target in `Release|x64`.

### 4.2 CMake command-line method (zlib)

#### Static libraries

```bat
cmake -S C:\dev\src\zlib -B C:\dev\build\zlib-vs ^
  -G "Visual Studio 16 2019" -A x64 ^
  -DCMAKE_INSTALL_PREFIX=C:\dev\install\zlib ^
  -DBUILD_SHARED_LIBS=OFF

cmake --build C:\dev\build\zlib-vs --config Release --target INSTALL
```

#### Shared libraries

```bat
cmake -S C:\dev\src\zlib -B C:\dev\build\zlib-vs ^
  -G "Visual Studio 16 2019" -A x64 ^
  -DCMAKE_INSTALL_PREFIX=C:\dev\install\zlib ^
  -DBUILD_SHARED_LIBS=ON

cmake --build C:\dev\build\zlib-vs --config Release --target INSTALL
```

Expected outputs (example):

```text
C:\dev\install\zlib\include
C:\dev\install\zlib\lib
C:\dev\install\zlib\bin   (if shared build)
```

## 5) Build HDF5 with zlib support

If you need MATLAB v7.3 support in matio, HDF5 is required.

---

### 5.1 CMake GUI method (HDF5)

1. Open **CMake GUI**.
2. Source: `C:/dev/src/hdf5`
3. Build: `C:/dev/build/hdf5-vs`
4. Configure with VS generator and `x64`.
5. Set:
   - `CMAKE_INSTALL_PREFIX = C:/dev/install/hdf5`
   - `BUILD_SHARED_LIBS = OFF` (static) **or** `ON` (shared)
   - `HDF5_ENABLE_Z_LIB_SUPPORT = ON`
   - `ZLIB_ROOT = C:/dev/install/zlib`
6. Generate.
7. Open the generated solution and build `INSTALL` in `Release|x64`.

### 5.2 CMake command-line method (HDF5)

#### Static libraries

```bat
cmake -S C:\dev\src\hdf5 -B C:\dev\build\hdf5-vs ^
  -G "Visual Studio 16 2019" -A x64 ^
  -DCMAKE_INSTALL_PREFIX=C:\dev\install\hdf5 ^
  -DBUILD_SHARED_LIBS=OFF ^
  -DHDF5_ENABLE_Z_LIB_SUPPORT=ON ^
  -DZLIB_ROOT=C:\dev\install\zlib

cmake --build C:\dev\build\hdf5-vs --config Release --target INSTALL
```

#### Shared libraries

```bat
cmake -S C:\dev\src\hdf5 -B C:\dev\build\hdf5-vs ^
  -G "Visual Studio 16 2019" -A x64 ^
  -DCMAKE_INSTALL_PREFIX=C:\dev\install\hdf5 ^
  -DBUILD_SHARED_LIBS=ON ^
  -DHDF5_ENABLE_Z_LIB_SUPPORT=ON ^
  -DZLIB_ROOT=C:\dev\install\zlib

cmake --build C:\dev\build\hdf5-vs --config Release --target INSTALL
```

Expected outputs (example):

```text
C:\dev\install\hdf5\include
C:\dev\install\hdf5\lib
C:\dev\install\hdf5\cmake
```

## 6) Build matio with HDF5 + zlib

Now configure matio to use both dependencies.

---

### 6.1 CMake GUI method (matio)

1. Open **CMake GUI**.
2. Source: `C:/dev/src/matio`
3. Build: `C:/dev/build/matio-vs`
4. Configure with VS generator and `x64`.
5. Set:
   - `CMAKE_INSTALL_PREFIX = C:/dev/install/matio`
   - `MATIO_WITH_ZLIB = ON`
   - `MATIO_WITH_HDF5 = ON`
   - `ZLIB_ROOT = C:/dev/install/zlib`
   - `HDF5_ROOT = C:/dev/install/hdf5`
   - `MATIO_SHARED = OFF` (static) **or** `ON` (shared)
6. If auto-detection fails, set explicit values:
   - `ZLIB_INCLUDE_DIR = C:/dev/install/zlib/include`
   - `ZLIB_LIBRARY = C:/dev/install/zlib/lib/<zlib_lib_name>.lib`
   - `HDF5_DIR = C:/dev/install/hdf5/cmake` (or package config directory)
7. Generate.
8. Open generated solution and build `INSTALL` in `Release|x64`.

### 6.2 CMake command-line method (matio)

#### Static matio

```bat
cmake -S C:\dev\src\matio -B C:\dev\build\matio-vs ^
  -G "Visual Studio 16 2019" -A x64 ^
  -DCMAKE_INSTALL_PREFIX=C:\dev\install\matio ^
  -DMATIO_WITH_ZLIB=ON ^
  -DMATIO_WITH_HDF5=ON ^
  -DZLIB_ROOT=C:\dev\install\zlib ^
  -DHDF5_ROOT=C:\dev\install\hdf5 ^
  -DMATIO_SHARED=OFF

cmake --build C:\dev\build\matio-vs --config Release --target INSTALL
```

#### Shared matio

```bat
cmake -S C:\dev\src\matio -B C:\dev\build\matio-vs ^
  -G "Visual Studio 16 2019" -A x64 ^
  -DCMAKE_INSTALL_PREFIX=C:\dev\install\matio ^
  -DMATIO_WITH_ZLIB=ON ^
  -DMATIO_WITH_HDF5=ON ^
  -DZLIB_ROOT=C:\dev\install\zlib ^
  -DHDF5_ROOT=C:\dev\install\hdf5 ^
  -DMATIO_SHARED=ON

cmake --build C:\dev\build\matio-vs --config Release --target INSTALL
```

Expected outputs (example):

```text
C:\dev\install\matio\include
C:\dev\install\matio\lib
C:\dev\install\matio\bin   (if shared build)
```

## 7) Link matio in a Visual Studio C++ project

In your application project properties (`Release|x64`):

- **C/C++ → General → Additional Include Directories**
  - `C:\dev\install\matio\include`
  - `C:\dev\install\zlib\include`
  - `C:\dev\install\hdf5\include`

- **Linker → General → Additional Library Directories**
  - `C:\dev\install\matio\lib`
  - `C:\dev\install\zlib\lib`
  - `C:\dev\install\hdf5\lib`

- **Linker → Input → Additional Dependencies**
  - `matio.lib`
  - zlib/HDF5 libraries generated by your build (names can vary by version/configuration)

> If you built shared libraries, ensure required `.dll` files are in your executable folder or in `PATH`.

## 8) Validation checklist

### 8.1 Confirm installed files exist

```bat
dir C:\dev\install\zlib\include
dir C:\dev\install\hdf5\include
dir C:\dev\install\matio\include

dir C:\dev\install\zlib\lib
dir C:\dev\install\hdf5\lib
dir C:\dev\install\matio\lib
```

### 8.2 Validate CMake package discovery (optional)

```bat
cmake -S C:\dev\src\matio -B C:\dev\build\matio-check ^
  -G "Visual Studio 16 2019" -A x64 ^
  -DZLIB_ROOT=C:\dev\install\zlib ^
  -DHDF5_ROOT=C:\dev\install\hdf5
```

No missing-package errors indicates dependency discovery is working.

### 8.3 Smoke-test in your app

- Include matio headers in a small C/C++ source.
- Link against generated libraries.
- Build `Release|x64`.
- Optionally open/save a `.mat` file to verify runtime behavior.

## 9) Troubleshooting

- **Linker not found in Visual Studio project properties**: you are likely editing a static library project, not an EXE/DLL project.
- **Architecture mismatch**: ensure all components are built as `x64` and with the same runtime/toolset family.
- **Dependency not found in CMake**: provide explicit `*_ROOT`, `*_INCLUDE_DIR`, and `*_LIBRARY` paths.
- **MSVC/MinGW incompatibility**: do not mix MinGW `.a` libraries with MSVC builds; use MSVC-generated `.lib` files.

---

You now have a reproducible CMake + Visual Studio workflow for building **zlib**, **HDF5**, and **matio** on **64-bit Windows**, including both GUI and command-line paths and static/shared options.
