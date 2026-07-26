pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
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

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t devops-task-tracker:latest .'
            }
        }

        stage('List Images') {
            steps {
                sh 'docker images'
            }
        }
    }
}