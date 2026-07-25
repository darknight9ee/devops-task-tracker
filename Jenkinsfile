pipeline {
    agent any
    stages {
        stage(' Checkout') {
            steps {
                echo 'Checking out the code...'
                checkout scm
            }
        }
        stage('Python Setup') {
            steps {
                sh '''
                python3 --version
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }
    }
}