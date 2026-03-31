pipeline {
	agent any
	environment {
		EMAIL = 'assafboneh2@gmail.com'
		PYTHON = 'python3'
	}
	stages {
		stage('Update/Install packages in the NetMan') {
			steps {
				script {
					def my_packages = ['ncclient', 'pandas', 'ipaddress', 'netaddr', 'prettytable']
					for (pkg in my_packages) {
						sh "${PYTHON} -m pip install --upgrade ${pkg}"
					}
				}
			}
		}
		stage('Check netconf with pylint') {
			steps {
				script {
					sh "${PYTHON} -m pip install pylint"
					sh "/var/lib/jenkins/.local/bin/pylint --fail-under=5 netman_netconf_obj2.py"
				}
			}
		}
		stage('Run netman_netconf') {
			steps {
				script {
					sh "${PYTHON} netman_netconf_obj2.py"
				}
			}
		}
		stage('Unit Tests') {
			steps {
				script {
					sh "${PYTHON} -m unittest test_netman_netconf_obj2.py"
				}
			}
		}
	}
	post {
		always {
			mail to: EMAIL,
				 subject: "Jenkins Build: ${currentBuild.fullDisplayName}",
				 body: "My Build ${currentBuild.fullDisplayName}. Finished with result: ${currentBuild.currentResult}"
		}
	}
}
