#!/usr/bin/env groovy

def builders = [:]

timestamps {

builders['gcc'] = {
    node('docker') {
        checkout scm
        def image = docker.image('ogs6/gcc-conan-package-tools-qt:latest')
        image.pull()
        image.inside() {
            withCredentials([usernamePassword(
                credentialsId: 'conan',
                passwordVariable: 'pw',
                usernameVariable: 'user')]) {
                sh "CONAN_PASSWORD=$pw python build.py"
            }
        }
    }
}

builders['mac'] = {
    node('mac') {
        checkout scm
        withCredentials([usernamePassword(
            credentialsId: 'conan',
            passwordVariable: 'pw',
            usernameVariable: 'user')]) {
            sh "CONAN_PASSWORD=$pw python build.py"
        }
    }
}

parallel builders

node { step([$class: 'GitHubCommitStatusSetter']) }

}
