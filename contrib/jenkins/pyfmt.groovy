#!/usr/bin/groovy

/*
 * Install and run pyfmt
 *
 * code_dirs is a string representing the paths (space delimted) to pass to pyfmt
 */
def call(String code_dirs) {
    sh "pip3 install --quiet black isort"
    sh "curl -s -o pyfmt https://raw.githubusercontent.com/GooeeIOT/pyfmt/master/bin/pyfmt"
    sh "chmod +x pyfmt"
    sh "./pyfmt --check ${code_dirs}"
    sh "rm ./pyfmt"
}
