Conan package for Qt
--------------------------------------------

[![Build Status](https://travis-ci.org/osechet/conan-qt.svg?branch=stable/5.9.2)](https://travis-ci.org/osechet/conan-qt)

[![Build status](https://ci.appveyor.com/api/projects/status/gboj3x82d42eoasw/branch/release/5.9.2?svg=true)](https://ci.appveyor.com/project/osechet/conan-qt)

[ ![Download](https://api.bintray.com/packages/osechet/Conan/Qt%3Aosechet/images/download.svg?version=5.9.2%3Astable) ](https://bintray.com/osechet/Conan/Qt%3Aosechet/5.9.2%3Astable/link)

[Conan.io](https://conan.io) package for [Qt](https://www.qt.io) library. This package includes by default the Qt Base module (Core, Gui, Widgets, Network, ...). Others modules can be added using options.

The packages generated with this **conanfile** can be found in [bintray.com](https://bintray.com/osechet/Conan).

## Reuse the package

### Basic setup

```
$ conan install Qt/5.9.2@osechet/stable
```

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

```
    [requires]
    Qt/5.9.2@osechet/stable

    [options]
    Qt:shared=true # false
    # On Windows, you can choose the opengl mode, default is 'desktop'
    Qt:opengl=desktop # dynamic
    # If you need specific Qt modules, you can add them as follow:
    Qt:websockets=true
    Qt:xmlpatterns=true

    [generators]
    txt
    cmake
```

Complete the installation of requirements for your project running:

```
    conan install .
```

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.

## Develop the package

### Build packages

    $ pip install conan_package_tools
    $ python build.py

### Upload packages to server

    $ conan upload Qt/5.9.2@osechet/stable --all
