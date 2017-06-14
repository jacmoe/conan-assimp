from conans import ConanFile, CMake, tools
from conans.tools import download, unzip, replace_in_file
import os


class AssimpConan(ConanFile):
    name = "Assimp"
    version = "3.3.1"
    license = "MIT"
    url = "https://github.com/jacmoe/conan-assimp"
    description = "Conan package for Assmip"
    requires = "zlib/1.2.8@lasote/stable"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        zip_name = "v%s.zip" % self.version
        download("https://github.com/assimp/assimp/archive/%s" % zip_name, zip_name, verify=False)
        unzip(zip_name)
        os.unlink(zip_name)
        self.run("cd assimp-3.3.1")
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("assimp-3.3.1/CMakeLists.txt", "PROJECT( Assimp )", '''PROJECT( Assimp )
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        assoptions = "-DASSIMP_BUILD_TESTS=OFF -DASSIMP_BUILD_SAMPLES=OFF"
        fixes = "-DCMAKE_CXX_FLAGS=-fPIC -DCMAKE_C_FLAGS=-fPIC"
        self.run('cmake assimp-3.3.1 %s %s %s %s' % (cmake.command_line, shared, assoptions, fixes))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="assimp-3.3.1/include")
        self.copy("*.hpp", dst="include", src="assimp-3.3.1/include")
        self.copy("*.inl", dst="include", src="assimp-3.3.1/include")
        self.copy("*assimp.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["assimp"]
        is_apple = (self.settings.os == 'Macos' or self.settings.os == 'iOS')
        if self.settings.build_type == "Debug" and not is_apple:
            self.cpp_info.libs = [lib+'d' for lib in self.cpp_info.libs]
        
        if self.settings.os == "Windows":
            self.cpp_info.cppflags.append("/EHsc")
            self.cpp_info.exelinkflags.append('-NODEFAULTLIB:LIBCMTD')
            self.cpp_info.exelinkflags.append('-NODEFAULTLIB:LIBCMT')
        else:
            self.cpp_info.cppflags.append("-std=c++11")

        if self.settings.os == "Macos":
            self.cpp_info.cppflags.append("-stdlib=libc++")
