[ ![Download](https://api.bintray.com/packages/slidewavellc/conan-libs/Assimp%3Aslidewave/images/download.svg) ](https://bintray.com/slidewavellc/conan-libs/Assimp%3Aslidewave/_latestVersion) 

Travis : [![Build Status](https://travis-ci.org/cinderblocks/conan-assimp.svg?branch=master)](https://travis-ci.org/cinderblocks/conan-assimp)

AppVeyor : [![Build status](https://ci.appveyor.com/api/projects/status/k8hdn6w8eafkp7yv?svg=true)](https://ci.appveyor.com/project/cinderblocks57647/conan-assimp)


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
