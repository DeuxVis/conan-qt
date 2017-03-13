#!/usr/bin/env groovy

def builders = [:]
def script="CONAN_UPLOAD=1 CONAN_REFERENCE=Qt/5.6.2 CONAN_USERNAME=bilke CONAN_CHANNEL=testing python build.py"

timestamps {

// builders['gcc'] = {
    // node('docker') {
        // checkout scm
        // def image = docker.image('ogs6/gcc-conan-package-tools-qt:latest')
        // image.pull()
        // image.inside() {
            // withCredentials([usernamePassword(
                // credentialsId: 'conan',
                // passwordVariable: 'pw',
                // usernameVariable: 'user')]) {
                // sh "CONAN_PASSWORD=$pw python build.py"
            // }
        // }
    // }
// }

builders['mac'] = {
    node('mac') {
        checkout scm
        withCredentials([usernamePassword(
            credentialsId: 'conan',
            passwordVariable: 'pw',
            usernameVariable: 'user')]) {
            sh "CONAN_PASSWORD=$pw ${script}"
        }
    }
}

builders['win'] = {
    node('win') {
        checkout scm
        withCredentials([usernamePassword(
            credentialsId: 'conan',
            passwordVariable: 'pw',
            usernameVariable: 'user')]) {
            sh "CONAN_PASSWORD=$pw ${script}"
        }
    }
}

parallel builders

}
