from conan.packager import ConanMultiPackager
from conans.tools import os_info
import platform

if __name__ == "__main__":
    builder = ConanMultiPackager(username="bilke", channel="testing")
    builder.add_common_builds()

    # Add xmlpatterns builds
    builder.add({"arch": "x86_64"}, {"Qt:xmlpatterns": "True"})

    # Filter out
    #  - macOS Debug builds
    #  - x32 builds
    filtered_builds = []
    for settings, options in builder.builds:
        if os_info.is_macos and settings["build_type"] == "Debug" \
            or settings["arch"] == "x86":
            continue
        filtered_builds.append([settings, options])
    builder.builds = filtered_builds

    builder.run()
