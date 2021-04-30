#! groovy

@Library('gcs-build-scripts') _

def SOURCE_TARBALL_NAME = "8bc3d38c43d80d0910dd04d592a880cf85ef6e4b.tar.gz"
def SOURCE_TARBALL_URL = "https://github.com/SpectraLogic/ds3_c_sdk/archive/${SOURCE_TARBALL_NAME}"


pipeline {
    agent none
    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
        timeout(time: 3, unit: 'HOURS')
        disableConcurrentBuilds()
    }
    stages {
        stage ("Prepare Source") {
            agent any
            steps {
                checkout scm
                script {
                    env.PACKAGE = "libds3v5"
                    env.PACKAGE_VERSION = "5.0.0"

                    env.SOURCE_STASH = "${UUID.randomUUID()}"

                    dirs (path: env.SOURCE_STASH, clean: true) {
                        sh """#! /bin/sh
                            set -e
                            curl -LOs "${SOURCE_TARBALL_URL}"
                            cp ../packaging/fedora/libds3v5.spec .
                            cp -R ../packaging/debian/libds3v5/debian debian
                        """
                    }
                    stash(name: env.SOURCE_STASH, includes: "${env.SOURCE_STASH}/**/*")
                }
            }
        }
        stage ("Build Packages") {
            steps {
                script {
                    parallel "debian": {
                        env.DEB_ARTIFACTS_STASH = buildDebian(
                                env.SOURCE_STASH,
                                SOURCE_TARBALL_NAME,
                                false,
                                getClubhouseEpic())
                    }, "rpm": {
                        env.RPM_ARTIFACTS_STASH = buildMock(
                            env.SOURCE_STASH,
                            SOURCE_TARBALL_NAME,
                            false,
                            getClubhouseEpic())
                    }, "failFast": false
                }
            }
        }
        stage ("Publish Results") {
            agent { label "master" }
            steps {
                script {
                    def stashname = "${UUID.randomUUID()}"

                    dir("artifacts") {
                        if (env.DEB_ARTIFACTS_STASH) {
                            unstash(name: env.DEB_ARTIFACTS_STASH)
                        }
                        if (env.RPM_ARTIFACTS_STASH) {
                            unstash(name: env.RPM_ARTIFACTS_STASH)
                        }
                        dir("source") {
                            unstash(name: env.SOURCE_STASH)
                            sh """rm -rf *.spec debian"""
                        }
                        stash(name: stashname, includes: "**/*")
                        deleteDir()
                    }
                    publishResults(
                        stashname,
                        env.PACKAGE,
                        env.PACKAGE_VERSION,
                        false)
                }
            }
        }
    }
}
