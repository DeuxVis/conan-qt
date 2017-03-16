#!/usr/bin/env groovy
@Library('conan-pipeline') _

def build = new conan.build()

timestamps {
    build.linux(
        conanReference: "Qt/5.6.2"
    )
}
