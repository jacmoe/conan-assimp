from conans import ConanFile, CMake, tools
from conans.tools import download, unzip, replace_in_file
import os


class AssimpConan(ConanFile):
    name = "Assimp"
    version = "3.3.1"
    license = "MIT"
    url = "https://github.com/jacmoe/conan-assimp"
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
        self.run('cmake assimp-3.3.1 %s %s' % (cmake.command_line, shared))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="assimp-3.3.1")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["assimp"]
