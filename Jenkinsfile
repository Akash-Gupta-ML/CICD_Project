pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'akashgupta0408/weather-app' // Your Docker Hub image
        DOCKER_CREDENTIALS = credentials('docker-credentials') // Docker credentials ID
        AWS_CREDENTIALS = credentials('aws-credentials') // AWS credentials ID
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    // Checkout code from the repository
                    checkout([$class: 'GitSCM', 
                        branches: [[name: '*/main']], 
                        userRemoteConfigs: [[url: 'https://github.com/Akash-Gupta-ML/Python-Project.git']]
                    ])
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image using the Jenkins build number
                    sh "docker build -t ${DOCKER_IMAGE}:${env.BUILD_NUMBER} -f weather_app/Dockerfile weather_app"
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Log in to Docker Hub
                    withCredentials([usernamePassword(credentialsId: 'docker-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh 'echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin'
                        // Push the image to Docker Hub
                        sh "docker push ${DOCKER_IMAGE}:${env.BUILD_NUMBER}" // Use double quotes for variable interpolation
                    }
                }
            }
        }
    
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Set the Kubernetes context (if necessary)
                    sh 'kubectl config use-context akash@test.us-east-1.eksctl.io'
                    sh 'sudo -u jenkins kubectl get pods --kubeconfig=/home/akash/.kube/config'
                    
                    // Update the Kubernetes deployment with the new image
                    sh "sudo -u jenkins kubectl set image deployment/weather-app weather-app=${DOCKER_IMAGE}:${env.BUILD_NUMBER} --record --kubeconfig=/home/akash/.kube/config"
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the logs for details.'
        }
    }
}
