
from conan import ConanFile, tools
from conan.tools.files import chdir
from conan.tools.cmake import cmake_layout
from conan.tools.scm import Git
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.env import VirtualRunEnv
from conan.tools.files import load, update_conandata

import os

class cllLicensecc(ConanFile):
    name = "licensecc"
    version = "1.0"
    license = "<Put your package license here>"
    url = "<Package recipe repository url here, for issues, etc.>"
    description = "Your library description"
    settings = "os", "compiler", "build_type", "arch"
    #generators = "CMakeDeps", "VirtualRunEnv"  # Exclude CMakeToolchain

    no_copy_source = True
    exports_sources = "*"
    
    default_options = {
        "boost/*:without_python": False,
        "boost/*:without_numpy": True
    }

    def source(self):
        self.output.info("Using source code from the local folder without copying.")
        return
        git = Git(self)
        git.clone("https://github.com/open-license-manager/licensecc.git", target=".")

    def requirements(self):
        self.requires("boost/1.83.0")

    def layout(self):
        print("CLL CONAN layout")
        cmake_layout(self)
        print("CLL CONAN layout done")

    def generate(self):
        print("CLL CONAN generate")
        
        # Explicitly instantiate and configure CMakeToolchain
        cmake_toolchain = CMakeToolchain(self)
        cmake_toolchain.variables["LCC_PROJECT_NAME"] = "NGSA"
        cmake_toolchain.variables["LCC_PROJECT_MAGIC_NUM"] = "98634"
        cmake_toolchain.generate()
        
        # Generate dependencies
        cmake = CMakeDeps(self)
        cmake.generate()

        # Generate virtual environment
        ms = VirtualRunEnv(self)
        ms.generate()
        print("CLL CONAN generate done")

    def build(self):
        print("CLL CONAN build")
        cmake = CMake(self)
        # cmake.configure(source_dir=self.source_folder)
        cmake_hardcoded_values = {"LCC_PROJECT_NAME":"NGSA", "LCC_PROJECT_MAGIC_NUM": 98634}
        cmake.configure( cmake_hardcoded_values )
        #cmake.configure()
        cmake.build()
        print("CLL CONAN build")
            
    def package(self):
        print("CLL CONAN pacakge")
        cmake = CMake(self)
        cmake.install()
        print("CLL CONAN pacakge done")

    def package_info(self):
        print("CLL CONAN package info")
        self.cpp_info.components["licensecc"].libs = ["licensecc"]
        self.cpp_info.components["licensecc"].set_property("cmake_target_name", "licensecc")