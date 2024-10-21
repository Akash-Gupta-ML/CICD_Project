pipeline {
    agent any
    stages {
        stage('Git Checkout') {
            steps {
                script {
                    checkout([$class: 'GitSCM', 
                        branches: [[name: '*/main']], 
                        userRemoteConfigs: [[url: 'https://github.com/Akash-Gupta-ML/CICD_Project.git']]
                    ])
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    def imageTag = "akashgupta0408/weather-app:${env.BUILD_NUMBER}"
                    // Point to the correct directory where the Dockerfile is located
                    sh "docker build --no-cache -t ${imageTag} -f ./CICD_Project"
                }
            }
        }
        stage('Push to Docker Hub') {
            steps {
                script {
                    def imageTag = "akashgupta0408/weather-app:${env.BUILD_NUMBER}"
                    withCredentials([usernamePassword(credentialsId: 'docker-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                        sh "docker push ${imageTag}"
                    }
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    def imageTag = "akashgupta0408/weather-app:${env.BUILD_NUMBER}"
                    // Update the image tag in your deployment YAML
                    sh "sed -i 's|image: akashgupta0408/weather-app:.*|image: ${imageTag}|g' kubernetes/deploy.yml"
                    sh 'kubectl config use-context kind-kind'
                    sh 'kubectl apply -f kubernetes/deploy.yml'
                    sh 'kubectl apply -f kubernetes/service.yml'
                    // Rollout the deployment
                    sh 'kubectl rollout status deployment/weather-app'
                    sh 'sudo -u jenkins kubectl port-forward svc/weather-app 31224:80 --address 0.0.0.0 &'
                }
            }
        }
    }
}
