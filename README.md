[ ![Download](https://api.bintray.com/packages/jacmoe/Conan/Assimp%3Ajacmoe/images/download.svg) ](https://bintray.com/jacmoe/Conan/Assimp%3Ajacmoe/_latestVersion)

Travis : [![Build Status](https://travis-ci.org/jacmoe/conan-assimp.svg?branch=master)](https://travis-ci.org/jacmoe/conan-assimp)

AppVeyor : [![Build status](https://ci.appveyor.com/api/projects/status/tsymtu12n2txr0um/branch/master?svg=true)](https://ci.appveyor.com/project/jacmoe/conan-assimp/branch/master)


# conan-assimp
Conan.io package for Assimp

### Basic setup

```
$ conan install Assimp/4.1.0@jacmoe/testing
```

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
```
    [requires]
    Assimp/4.1.0@jacmoe/testing

    [options]
    Assimp:shared=True # False

    [generators]
    txt
    cmake
```
Complete the installation of requirements for your project running:
```
    conan install .
```
Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
