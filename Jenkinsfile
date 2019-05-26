
pipeline {
  agent any
  stages {

	  stage('Pull on server') {
	    steps {
	      withCredentials(bindings: [sshUserPrivateKey(credentialsId: 'jenkins_for_github', keyFileVariable: 'FILE', passphraseVariable: '', usernameVariable: '')]) {
	        dir(path: '/srv/1-workspace/notebooks/tensorflow-models') {
	          sh '''
	                      git config --local core.sshCommand \'ssh -vvv -i $FILE\'
	                      git config --local user.name "Baptiste Bouffaut"
	                      git config --local user.email "baptiste.bouffaut@gmail.com"

	                      git fetch origin
	                      git checkout ${GIT_BRANCH}


	                      git reset --hard origin/${GIT_BRANCH}

	                 '''
	        }

	      }

	    }
	  }

	}
}
