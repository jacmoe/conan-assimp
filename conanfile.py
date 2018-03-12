from conans import ConanFile, CMake, tools
import os


class AssimpConan(ConanFile):
    name = "Assimp"
    version = "4.1.0"
    license = "BSD 3-Clause"
    homepage = "https://github.com/assimp/assimp"
    url = "https://github.com/jacmoe/conan-assimp"
    description = "Conan package for Assmip"
    requires = "zlib/1.2.11@conan/stable"
    settings = "os", "compiler", "build_type", "arch"
    source_subfolder = "sources"
    options = {
        "shared": [True, False],
        "double_precision": [True, False],
        "no_export": [True, False],
        "internal_irrxml": [True, False],
        "fPIC": [True, False],
    }
    # only fPIC enabled by default
    default_options = ("=False\n".join(options.keys()) + "=False\n").replace("fPIC=False", "fPIC=True")
    format_option_map = {
        "with_3d": "ASSIMP_BUILD_3D_IMPORTER",
        "with_3ds": "ASSIMP_BUILD_3DS_IMPORTER",
        "with_3mf": "ASSIMP_BUILD_3MF_IMPORTER",
        "with_ac": "ASSIMP_BUILD_AC_IMPORTER",
        "with_amf": "ASSIMP_BUILD_AMF_IMPORTER",
        "with_ase": "ASSIMP_BUILD_ASE_IMPORTER",
        "with_assbin": "ASSIMP_BUILD_ASSBIN_IMPORTER",
        "with_assxml": "ASSIMP_BUILD_ASSXML_IMPORTER",
        "with_b3d": "ASSIMP_BUILD_B3D_IMPORTER",
        "with_blend": "ASSIMP_BUILD_BLEND_IMPORTER",
        "with_bvh": "ASSIMP_BUILD_BVH_IMPORTER",
        "with_cob": "ASSIMP_BUILD_COB_IMPORTER",
        "with_collada": "ASSIMP_BUILD_COLLADA_IMPORTER",
        "with_csm": "ASSIMP_BUILD_CSM_IMPORTER",
        "with_dxf": "ASSIMP_BUILD_DXF_IMPORTER",
        "with_fbx": "ASSIMP_BUILD_FBX_IMPORTER",
        "with_gltf": "ASSIMP_BUILD_GLTF_IMPORTER",
        "with_hmp": "ASSIMP_BUILD_HMP_IMPORTER",
        "with_ifc": "ASSIMP_BUILD_IFC_IMPORTER",
        "with_irr": "ASSIMP_BUILD_IRR_IMPORTER",
        "with_irrmesh": "ASSIMP_BUILD_IRRMESH_IMPORTER",
        "with_lwo": "ASSIMP_BUILD_LWO_IMPORTER",
        "with_lws": "ASSIMP_BUILD_LWS_IMPORTER",
        "with_md2": "ASSIMP_BUILD_MD2_IMPORTER",
        "with_md3": "ASSIMP_BUILD_MD3_IMPORTER",
        "with_md5": "ASSIMP_BUILD_MD5_IMPORTER",
        "with_mdc": "ASSIMP_BUILD_MDC_IMPORTER",
        "with_mdl": "ASSIMP_BUILD_MDL_IMPORTER",
        "with_mmd": "ASSIMP_BUILD_MMD_IMPORTER",
        "with_ms3d": "ASSIMP_BUILD_MS3D_IMPORTER",
        "with_ndo": "ASSIMP_BUILD_NDO_IMPORTER",
        "with_nff": "ASSIMP_BUILD_NFF_IMPORTER",
        "with_obj": "ASSIMP_BUILD_OBJ_IMPORTER",
        "with_off": "ASSIMP_BUILD_OFF_IMPORTER",
        "with_ogre": "ASSIMP_BUILD_OGRE_IMPORTER",
        "with_opengex": "ASSIMP_BUILD_OPENGEX_IMPORTER",
        "with_ply": "ASSIMP_BUILD_PLY_IMPORTER",
        "with_q3bsp": "ASSIMP_BUILD_Q3BSP_IMPORTER",
        "with_q3d": "ASSIMP_BUILD_Q3D_IMPORTER",
        "with_raw": "ASSIMP_BUILD_RAW_IMPORTER",
        "with_sib": "ASSIMP_BUILD_SIB_IMPORTER",
        "with_smd": "ASSIMP_BUILD_SMD_IMPORTER",
        "with_stl": "ASSIMP_BUILD_STL_IMPORTER",
        "with_terragen": "ASSIMP_BUILD_TERRAGEN_IMPORTER",
        "with_x": "ASSIMP_BUILD_X_IMPORTER",
        "with_x3d": "ASSIMP_BUILD_X3D_IMPORTER",
        "with_xgl": "ASSIMP_BUILD_XGL_IMPORTER",
    }
    options.update(dict.fromkeys(format_option_map, [True, False]))
    # All format options enabled by default
    default_options += "=True\n".join(format_option_map.keys()) + "=True"
    generators = "cmake"
    exports = ["LICENSE.md"]
    exports_sources = ["patches/*"]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def requirements(self):
        if not self.options.internal_irrxml:
            # Using requirement from conan-center
            self.requires("IrrXML/1.2@conan/stable")

    def source(self):
        source_url = "%s/archive/v%s.zip" % (self.homepage, self.version)
        tools.get(source_url)
        os.rename("assimp-%s" % (self.version,), self.source_subfolder)

        # clang and compiler.libcxx=libc++ build fails due to <cstdlib> is not included. Fixed in HEAD/master
        tools.patch(patch_file="patches/Q3BSPZipArchive.cpp.patch")

        tools.replace_in_file("%s/CMakeLists.txt" % self.source_subfolder, "PROJECT( Assimp )", '''PROJECT( Assimp )
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()""")

    def build(self):
        cmake = CMake(self)
        # Use conan-irrxml instead of irrxml included in assimp
        cmake.definitions["SYSTEM_IRRXML"] = not self.options.internal_irrxml

        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["ASSIMP_DOUBLE_PRECISION"] = self.options.double_precision
        cmake.definitions["ASSIMP_NO_EXPORT"] = self.options.no_export
        cmake.definitions["ASSIMP_BUILD_ASSIMP_TOOLS"] = False
        cmake.definitions["ASSIMP_BUILD_TESTS"] = False
        cmake.definitions["ASSIMP_BUILD_SAMPLES"] = False
        cmake.definitions["ASSIMP_INSTALL_PDB"] = False

        # Disabling ASSIMP_ANDROID_JNIIOSYSTEM, failing in cmake install
        cmake.definitions["ASSIMP_ANDROID_JNIIOSYSTEM"] = False

        if self.settings.os != "Windows":
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC

        # Enable/Disable format importer options in cmake
        cmake.definitions["ASSIMP_BUILD_ALL_IMPORTERS_BY_DEFAULT"] = False
        for option, definition in self.format_option_map.items():
            cmake.definitions[definition] = bool(getattr(self.options, option))

        cmake.configure(source_folder=self.source_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        # There are more than one LICENSE in source tree, choosing package and src license
        self.copy("LICENSE.md", dst="licenses", keep_path=False)
        self.copy("LICENSE", dst="licenses", src=self.source_subfolder, keep_path=False)
        include_folder = os.path.join(self.source_subfolder, "include")
        self.copy("*.h", dst="include", src=include_folder)
        self.copy("*.hpp", dst="include", src=include_folder)
        self.copy("*.inl", dst="include", src=include_folder)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.lib", src="lib", dst="lib", keep_path=False)

        if self.options.shared:
            self.copy("*.dll", src="bin", dst="bin", keep_path=False)
            self.copy("*.so*", dst="lib", keep_path=False)
            self.copy("*.dylib*", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
