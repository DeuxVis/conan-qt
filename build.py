from conan.packager import ConanMultiPackager
from conans.tools import os_info
import platform

if __name__ == "__main__":
    builder = ConanMultiPackager(username="bilke", channel="testing")
    builder.add_common_builds()

    # Add xmlpatterns builds
    builder.add({"arch": "x86", "build_type": "Release"}, {"Qt:xmlpatterns": "True"})
    builder.add({"arch": "x86_64", "build_type": "Release"}, {"Qt:xmlpatterns": "True"})
    builder.add({"arch": "x86_64", "build_type": "Debug"}, {"Qt:xmlpatterns": "True"})
    builder.add({"arch": "x86_64", "build_type": "Debug", "compiler": "Visual Studio", "compiler.runtime": "MDd"}, {"Qt:xmlpatterns": "True"})

    # Filter out
    #  - macOS Debug builds
    #  - x32 builds
    filtered_builds = []
    for settings, options in builder.builds:
        if (os_info.is_macos and settings["build_type"] == "Debug") \
            or (not os_info.is_windows and settings["arch"] == "x86"):
            continue
        filtered_builds.append([settings, options])
    builder.builds = filtered_builds

    builder.run()
