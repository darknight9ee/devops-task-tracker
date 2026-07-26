pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Build Environment') {
            steps {
                sh 'git --version'
                sh 'python3 --version'
                sh 'docker --version'
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                    python -m pytest
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t devops-task-tracker:latest .'
            }
        }

    }
}