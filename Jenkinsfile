
pipeline {
  agent any
  stages {

	  stage('Pull on server') {
	    steps {
	      withCredentials(bindings: [sshUserPrivateKey(credentialsId: 'jenkins', keyFileVariable: 'FILE', passphraseVariable: '', usernameVariable: '')]) {
	        dir(path: '/srv/1-workspace/notebooks/tensorflow-models') {
	          sh '''
	                      git config core.sshCommand \'ssh -i $FILE\'
	                      git config  user.name "Baptiste Bouffaut"
	                      git config user.email "baptiste.bouffaut@gmail.com"

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
