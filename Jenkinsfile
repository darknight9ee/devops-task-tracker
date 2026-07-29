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
                docker build -t $IMAGE_NAME:${BUILD_NUMBER} .
                docker tag $IMAGE_NAME:${BUILD_NUMBER} $IMAGE_NAME:latest
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

                    docker push $IMAGE_NAME:${BUILD_NUMBER}
                    docker push $IMAGE_NAME:latest

                    docker logout
                    '''
                }
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                cd /home/ubuntu/deployment

                echo IMAGE_TAG=${BUILD_NUMBER} > image.env

                docker compose --env-file image.env pull

                docker compose --env-file image.env up -d
                '''
            }
        }
        stage('Health Check') {
            steps {
                sh '''
                sleep 20

                docker exec task-tracker \
                curl --fail http://localhost:5000/health
                '''
            }
        }
    }
}