[ ![Download](https://api.bintray.com/packages/slidewavellc/conan-libs/Assimp%3Aslidewave/images/download.svg) ](https://bintray.com/slidewavellc/conan-libs/Assimp%3Aslidewave/_latestVersion) 

Travis : [![Build Status](https://travis-ci.org/pvicente/conan-assimp.svg?branch=testing%2F4.0.1)](https://travis-ci.org/pvicente/conan-assimp)

AppVeyor : [![Build status](https://ci.appveyor.com/api/projects/status/janqy71mtspxctgw/branch/testing/4.0.1?svg=true)](https://ci.appveyor.com/project/pvicente/conan-assimp/branch/testing/4.0.1)


# conan-assimp
Conan.io package for Assimp

### Basic setup

```
$ conan install Assimp/4.0.1@slidewave/stable
```

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
```
    [requires]
    Assimp/4.0.1@slidewave/stable

    [options]
    Assimp:shared=true # false

    [generators]
    txt
    cmake
```
Complete the installation of requirements for your project running:
```
    conan install .
```
Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
