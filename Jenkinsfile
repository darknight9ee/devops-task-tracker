pipeline {
    agent any

    environment {
        IMAGE_NAME = "darknight9ee/devops-task-tracker"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                . venv/bin/activate
                python -m flake8 .
                '''
            }
        }

        stage('Tests') {
            steps {
                sh '''
                . venv/bin/activate
                python -m pytest
                '''
            }
        }

        stage('Build Image') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME:latest .
                docker tag $IMAGE_NAME:latest $IMAGE_NAME:${BUILD_NUMBER}
                '''
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                        docker push darknight9ee/devops-task-tracker:latest

                        docker logout
                    '''
                }
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                docker compose down

                docker compose pull

                docker compose up -d
                '''
            }
        }
        stage('Health Check') {
            steps {
                sh '''
                sleep 20

                curl --fail http://localhost:5000/health
                '''
            }
        }
    }
}