[ ![Download](https://api.bintray.com/packages/pvicente/conan/Assimp%3Apvicente/images/download.svg?version=3.3.1%3Atesting) ](https://bintray.com/pvicente/conan/Assimp%3Apvicente/3.3.1%3Atesting/link)

Travis : [![Build Status](https://travis-ci.org/pvicente/conan-assimp.svg?branch=testing%2F3.3.1)](https://travis-ci.org/pvicente/conan-assimp)

AppVeyor : [![Build status](https://ci.appveyor.com/api/projects/status/janqy71mtspxctgw/branch/testing/3.3.1?svg=true)](https://ci.appveyor.com/project/pvicente/conan-assimp/branch/testing/3.3.1)



# conan-assimp
Conan.io package for Assimp

### Basic setup

```
$ conan install Assimp/3.3.1@jacmoe/testing
```

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
```
    [requires]
    Assimp/3.3.1@jacmoe/testing

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
