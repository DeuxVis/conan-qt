
import os
from distutils.spawn import find_executable
from conans import ConanFile, ConfigureEnvironment
from conans.tools import cpu_count, vcvars_command, os_info, SystemPackageTool

class QtConan(ConanFile):
    """ Qt Conan package """

    name = "Qt"
    version = "5.6.2"
    description = "Qt GUI libraries"
    sourceDir = "qt5"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "opengl": ["desktop", "dynamic"],
        "websockets": [True, False],
        "xmlpatterns": [True, False]
    }
    default_options = "shared=True", "opengl=desktop", "websockets=False", "xmlpatterns=False"
    url = "http://github.com/bilke/conan-qt"
    license = "http://doc.qt.io/qt-5/lgpl.html"
    short_paths = True

    def system_requirements(self):
        pack_names = None
        if os_info.linux_distro == "ubuntu":
            pack_names = ["libgl1-mesa-dev", "libxcb1", "libxcb1-dev",
                          "libx11-xcb1", "libx11-xcb-dev", "libxcb-keysyms1",
                          "libxcb-keysyms1-dev", "libxcb-image0", "libxcb-image0-dev",
                          "libxcb-shm0", "libxcb-shm0-dev", "libxcb-icccm4",
                          "libxcb-icccm4-dev", "libxcb-sync1", "libxcb-sync-dev",
                          "libxcb-xfixes0-dev", "libxrender-dev", "libxcb-shape0-dev",
                          "libxcb-randr0-dev", "libxcb-render-util0", "libxcb-render-util0-dev",
                          "libxcb-glx0-dev", "libxcb-xinerama0", "libxcb-xinerama0-dev"]

            if self.settings.arch == "x86":
                full_pack_names = []
                for pack_name in pack_names:
                    full_pack_names += [pack_name + ":i386"]
                pack_names = full_pack_names

        if pack_names:
            installer = SystemPackageTool()
            installer.update() # Update the package database
            installer.install(" ".join(pack_names)) # Install the package

    def source(self):
        major = ".".join(self.version.split(".")[:2])
        self.run("git clone https://code.qt.io/qt/qt5.git")
        self.run("cd %s && git checkout %s" % (self.sourceDir, major))
        if self.settings.os != "Windows":
            self.run("chmod +x ./%s/configure" % self.sourceDir)

    def build(self):
        """ Define your project building. You decide the way of building it
            to reuse it later in any other project.
        """

        submodules = ["qtbase"]
        if self.options.websockets:
            submodules.append("qtwebsockets")
        if self.options.xmlpatterns:
            submodules.append("qtxmlpatterns")

        self.run("cd %s && perl init-repository --no-update --module-subset=%s"
                 % (self.sourceDir, ",".join(submodules)))
        self.run("cd %s && git checkout v%s && git submodule update"
                 % (self.sourceDir, self.version))

        args = ["-opensource", "-confirm-license", "-nomake examples", "-nomake tests",
                "-no-icu", "-prefix %s" % self.package_folder]
        if not self.options.shared:
            args.insert(0, "-static")
        if self.settings.build_type == "Debug":
            args.append("-debug")
        else:
            args.append("-release")

        if self.settings.os == "Windows":
            if self.settings.compiler == "Visual Studio":
                self._build_msvc(args)
            else:
                self._build_mingw(args)
        else:
            self._build_unix(args)

    def _build_msvc(self, args):
        build_command = find_executable("jom.exe")
        if build_command:
            build_args = ["-j", str(cpu_count())]
        else:
            build_command = "nmake.exe"
            build_args = []
        self.output.info("Using '%s %s' to build" % (build_command, " ".join(build_args)))

        vcvars = vcvars_command(self.settings)
        vcvars = vcvars + " && " if vcvars else ""
        set_env = 'SET PATH={dir}/qtbase/bin;{dir}/gnuwin32/bin;%PATH%'.format(dir=self.conanfile_directory)
        args += ["-opengl %s" % self.options.opengl]
        # it seems not enough to set the vcvars for older versions, it works fine
        # with MSVC2015 without -platform
        if self.settings.compiler == "Visual Studio":
            if self.settings.compiler.version == "12":
                args += ["-platform win32-msvc2013"]
            if self.settings.compiler.version == "11":
                args += ["-platform win32-msvc2012"]
            if self.settings.compiler.version == "10":
                args += ["-platform win32-msvc2010"]

        self.run("cd %s && %s && %s configure %s"
                 % (self.sourceDir, set_env, vcvars, " ".join(args)))
        self.run("cd %s && %s %s %s"
                 % (self.sourceDir, vcvars, build_command, " ".join(build_args)))
        self.run("cd %s && %s %s install" % (self.sourceDir, vcvars, build_command))

    def _build_mingw(self, args):
        env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
        args += ["-developer-build", "-opengl %s" % self.options.opengl, "-platform win32-g++"]

        self.output.info("Using '%s' threads" % str(cpu_count()))
        self.run("%s && cd %s && configure.bat %s"
                 % (env.command_line_env, self.sourceDir, " ".join(args)))
        self.run("%s && cd %s && mingw32-make -j %s"
                 % (env.command_line_env, self.sourceDir, str(cpu_count())))
        self.run("%s && cd %s && mingw32-make install" % (env.command_line_env, self.sourceDir))

    def _build_unix(self, args):
        if self.settings.os == "Linux":
            args += ["-silent", "-xcb"]
            if self.settings.arch == "x86":
                args += ["-platform linux-g++-32"]
        else:
            args += ["-silent"]
            if self.settings.arch == "x86":
                args += ["-platform macx-clang-32"]

        self.output.info("Using '%s' threads" % str(cpu_count()))
        self.run("cd %s && ./configure %s" % (self.sourceDir, " ".join(args)))
        self.run("cd %s && make -j %s" % (self.sourceDir, str(cpu_count())))
        self.run("cd %s && make install" % (self.sourceDir))

    def package(self):
        pass # Everything is already copied by make install

    def package_info(self):
        libs = ['Concurrent', 'Core', 'DBus',
                'Gui', 'Network', 'OpenGL',
                'Sql', 'Test', 'Widgets', 'Xml']

        if self.options.websockets:
            libs.append("WebSockets")
        if self.options.xmlpatterns:
            libs.append("XmlPatterns")

        self.cpp_info.libs = []
        self.cpp_info.includedirs = ["include"]
        for lib in libs:
            if self.settings.os == "Windows" and self.settings.build_type == "Debug":
                suffix = "d"
            else:
                suffix = ""
            self.cpp_info.libs += ["Qt5%s%s" % (lib, suffix)]
            self.cpp_info.includedirs += ["include/Qt%s" % lib]

        if self.settings.os == "Windows":
            # Some missing shared libs inside QML and others, but for the test it works
            self.env_info.path.append(os.path.join(self.package_folder, "bin"))
