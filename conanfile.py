from conans import ConanFile, CMake, tools


class AssimpConan(ConanFile):
    name = "Assimp"
    version = "4.0.1"
    license = "MIT"
    homepage = "https://github.com/assimp/assimp"
    url = "https://github.com/jacmoe/conan-assimp"
    description = "Conan package for Assmip"
    requires = "zlib/1.2.11@conan/stable"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "double_precision": [True, False],
        "no_export": [True, False],
        "fPIC": [True, False]
        }
    default_options = "=False\n".join(options.keys()) + "=False\n"
    format_options = {
        "with_amf": [True, False],
        "with_3ds": [True, False],
        "with_ac": [True, False],
        "with_ase": [True, False],
        "with_assbin": [True, False],
        "with_assxml": [True, False],
        "with_b3d": [True, False],
        "with_bvh": [True, False],
        "with_collada": [True, False],
        "with_dxf": [True, False],
        "with_csm": [True, False],
        "with_hmp": [True, False],
        "with_irrmesh": [True, False],
        "with_irr": [True, False],
        "with_lwo": [True, False],
        "with_lws": [True, False],
        "with_md2": [True, False],
        "with_md3": [True, False],
        "with_md5": [True, False],
        "with_mdc": [True, False],
        "with_mdl": [True, False],
        "with_nff": [True, False],
        "with_ndo": [True, False],
        "with_off": [True, False],
        "with_obj": [True, False],
        "with_ogre": [True, False],
        "with_opengex": [True, False],
        "with_ply": [True, False],
        "with_ms3d": [True, False],
        "with_cob": [True, False],
        "with_blend": [True, False],
        "with_ifc": [True, False],
        "with_xgl": [True, False],
        "with_fbx": [True, False],
        "with_q3d": [True, False],
        "with_q3bsp": [True, False],
        "with_raw": [True, False],
        "with_sib": [True, False],
        "with_smd": [True, False],
        "with_stl": [True, False],
        "with_terragen": [True, False],
        "with_3d": [True, False],
        "with_x": [True, False],
        "with_x3d": [True, False],
        "with_gltf": [True, False],
        "with_3mf": [True, False],
        "with_mmd": [True, False]
        }
    default_format_options = "=True\n".join(format_options.keys()) + "=True"
    options.update(format_options)
    default_options += default_format_options
    generators = "cmake"
    exports = ["LICENSE.md"]
    exports_sources = "cmakefix.patch"

    def configure(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        self.run("git clone https://github.com/assimp/assimp.git")
        self.run("cd assimp && git checkout tags/v4.0.1")
        self.run("cp cmakefix.patch assimp && cd assimp && git apply cmakefix.patch")
        self.run("rm -r assimp/samples")
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("assimp/CMakeLists.txt", "PROJECT( Assimp )", '''PROJECT( Assimp )
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared 
        cmake.definitions["ASSIMP_DOUBLE_PRECISION"] = self.options.double_precision
        cmake.definitions["ASSIMP_NO_EXPORT"] = self.options.no_export
        cmake.definitions["ASSIMP_BUILD_ASSIMP_TOOLS"] = False
        cmake.definitions["ASSIMP_BUILD_TESTS"] = False
        cmake.definitions["ASSIMP_BUILD_SAMPLES"] = False
        cmake.definitions["ASSIMP_INSTALL_PDB"] = False
        if self.settings.os != "Windows":
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC

        # X3D Importer is broken on VS2017 for 4.0.1. Fixed in HEAD, so remove this next version
        if self.settings.compiler == "Visual Studio":
            self.options.with_x3d = False

        cmake.definitions["ASSIMP_BUILD_ALL_IMPORTERS_BY_DEFAULT"] = False
        if self.options.with_amf:
            cmake.definitions["ASSIMP_BUILD_AMF_IMPORTER"] = True
        if self.options.with_3ds:
            cmake.definitions["ASSIMP_BUILD_3DS_IMPORTER"] = True 
        if self.options.with_ac:
            cmake.definitions["ASSIMP_BUILD_AC_IMPORTER"] = True 
        if self.options.with_ase:
            cmake.definitions["ASSIMP_BUILD_ASE_IMPORTER"] = True 
        if self.options.with_assbin:
            cmake.definitions["ASSIMP_BUILD_ASSBIN_IMPORTER"] = True 
        if self.options.with_assxml:
            cmake.definitions["ASSIMP_BUILD_ASSXML_IMPORTER"] = True 
        if self.options.with_b3d:
            cmake.definitions["ASSIMP_BUILD_B3D_IMPORTER"] = True 
        if self.options.with_bvh:
            cmake.definitions["ASSIMP_BUILD_BVH_IMPORTER"] = True 
        if self.options.with_collada:
            cmake.definitions["ASSIMP_BUILD_COLLADA_IMPORTER"] = True 
        if self.options.with_dxf:
            cmake.definitions["ASSIMP_BUILD_DXF_IMPORTER"] = True 
        if self.options.with_csm:
            cmake.definitions["ASSIMP_BUILD_CSM_IMPORTER"] = True 
        if self.options.with_hmp:
            cmake.definitions["ASSIMP_BUILD_HMP_IMPORTER"] = True 
        if self.options.with_irrmesh:
            cmake.definitions["ASSIMP_BUILD_IRRMESH_IMPORTER"] = True 
        if self.options.with_irr:
            cmake.definitions["ASSIMP_BUILD_IRR_IMPORTER"] = True 
        if self.options.with_lwo:
            cmake.definitions["ASSIMP_BUILD_LWO_IMPORTER"] = True 
        if self.options.with_lws:
            cmake.definitions["ASSIMP_BUILD_LWS_IMPORTER"] = True 
        if self.options.with_md2:
            cmake.definitions["ASSIMP_BUILD_MD2_IMPORTER"] = True 
        if self.options.with_md3:
            cmake.definitions["ASSIMP_BUILD_MD3_IMPORTER"] = True 
        if self.options.with_md5:
            cmake.definitions["ASSIMP_BUILD_MD5_IMPORTER"] = True 
        if self.options.with_mdc:
            cmake.definitions["ASSIMP_BUILD_MDC_IMPORTER"] = True 
        if self.options.with_mdl:
            cmake.definitions["ASSIMP_BUILD_MDL_IMPORTER"] = True 
        if self.options.with_nff:
            cmake.definitions["ASSIMP_BUILD_NFF_IMPORTER"] = True 
        if self.options.with_ndo:
            cmake.definitions["ASSIMP_BUILD_NDO_IMPORTER"] = True 
        if self.options.with_off:
            cmake.definitions["ASSIMP_BUILD_OFF_IMPORTER"] = True 
        if self.options.with_obj:
            cmake.definitions["ASSIMP_BUILD_OBJ_IMPORTER"] = True 
        if self.options.with_ogre:
            cmake.definitions["ASSIMP_BUILD_OGRE_IMPORTER"] = True 
        if self.options.with_opengex:
            cmake.definitions["ASSIMP_BUILD_OPENGEX_IMPORTER"] = True 
        if self.options.with_ply:
            cmake.definitions["ASSIMP_BUILD_PLY_IMPORTER"] = True 
        if self.options.with_ms3d:
            cmake.definitions["ASSIMP_BUILD_MS3D_IMPORTER"] = True 
        if self.options.with_cob:
            cmake.definitions["ASSIMP_BUILD_COB_IMPORTER"] = True 
        if self.options.with_blend:
            cmake.definitions["ASSIMP_BUILD_BLEND_IMPORTER"] = True 
        if self.options.with_ifc:
            cmake.definitions["ASSIMP_BUILD_IFC_IMPORTER"] = True 
        if self.options.with_xgl:
            cmake.definitions["ASSIMP_BUILD_XGL_IMPORTER"] = True 
        if self.options.with_fbx:
            cmake.definitions["ASSIMP_BUILD_FBX_IMPORTER"] = True 
        if self.options.with_q3d:
            cmake.definitions["ASSIMP_BUILD_Q3D_IMPORTER"] = True 
        if self.options.with_q3bsp:
            cmake.definitions["ASSIMP_BUILD_Q3BSP_IMPORTER"] = True 
        if self.options.with_raw:
            cmake.definitions["ASSIMP_BUILD_RAW_IMPORTER"] = True 
        if self.options.with_sib:
            cmake.definitions["ASSIMP_BUILD_SIB_IMPORTER"] = True 
        if self.options.with_smd:
            cmake.definitions["ASSIMP_BUILD_SMD_IMPORTER"] = True 
        if self.options.with_stl:
            cmake.definitions["ASSIMP_BUILD_STL_IMPORTER"] = True 
        if self.options.with_terragen:
            cmake.definitions["ASSIMP_BUILD_TERRAGEN_IMPORTER"] = True 
        if self.options.with_3d:
            cmake.definitions["ASSIMP_BUILD_3D_IMPORTER"] = True 
        if self.options.with_x:
            cmake.definitions["ASSIMP_BUILD_X_IMPORTER"] = True 
        if self.options.with_x3d:
            cmake.definitions["ASSIMP_BUILD_X3D_IMPORTER"] = True
        if self.options.with_gltf:
            cmake.definitions["ASSIMP_BUILD_GLTF_IMPORTER"] = True 
        if self.options.with_3mf:
            cmake.definitions["ASSIMP_BUILD_3MF_IMPORTER"] = True
        if self.options.with_mmd:
            cmake.definitions["ASSIMP_BUILD_MMD_IMPORTER"] = True

        cmake.configure(source_dir="assimp")
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*.h", dst="include", src="include")
        self.copy("*.hpp", dst="include", src="include")
        self.copy("*.inl", dst="include", src="include")
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.lib", src="lib", dst="lib", keep_path=False)

        if self.options.shared:
            self.copy("*.dll", src="bin", dst="bin", keep_path=False)
            self.copy("*.so*", dst="lib", keep_path=False)
            self.copy("*.dylib*", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
