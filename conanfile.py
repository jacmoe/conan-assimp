from conans import ConanFile, CMake, tools
import os


class AssimpConan(ConanFile):
    name = "Assimp"
    version = "3.3.1"
    license = "BSD 3-Clause"
    homepage = "https://github.com/assimp/assimp"
    url = "https://github.com/jacmoe/conan-assimp"
    description = "Conan package for Assmip"
    requires = "zlib/1.2.11@conan/stable"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    source_subfolder = "sources"
    default_options = "shared=False", "fPIC=True"
    generators = "cmake"
    exports = ["LICENSE.md"]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        source_url = "%s/archive/v%s.zip" % (self.homepage, self.version)
        tools.get(source_url)
        os.rename("assimp-%s" % (self.version, ), self.source_subfolder)
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("%s/CMakeLists.txt" % (self.source_subfolder,), "PROJECT( Assimp )", """PROJECT( Assimp )
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()""")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["ASSIMP_BUILD_TESTS"] = "OFF"
        cmake.definitions["ASSIMP_BUILD_SAMPLES"] = "OFF"
        if self.settings.os != "Windows":
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.configure(source_folder=self.source_subfolder)
        cmake.build()

    def package(self):
        # There are more than one LICENSE in source tree, choosing package and src license
        self.copy("LICENSE.md", dst="licenses", keep_path=False)
        self.copy("LICENSE", dst="licenses", src=self.source_subfolder, keep_path=False)
        include_folder = os.path.join(self.source_subfolder, "include")
        self.copy("*.h", dst="include", src=include_folder)
        self.copy("*.hpp", dst="include", src=include_folder)
        self.copy("*.inl", dst="include", src=include_folder)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*assimp*.lib", src="lib", dst="lib", keep_path=False)

        if self.options.shared:
            self.copy("*.dll", src="bin", dst="bin", keep_path=False)
            self.copy("*assimp*.so*", dst="lib", keep_path=False)
            self.copy("*.dylib*", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
