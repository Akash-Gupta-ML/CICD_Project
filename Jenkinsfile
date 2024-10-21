pipeline {
    agent any
    stages {
        stage('Clone') {
            steps {
                script {
                    def repoUrl = 'https://github.com/Akash-Gupta-ML/CICD_Project.git'
                    def repoDir = 'CICD_Project'
                    
                    // Check if the directory already exists
                    if (fileExists(repoDir)) {
                        // If it exists, pull the latest changes
                        dir(repoDir) {
                            sh 'git pull origin master'
                        }
                    } else {
                        // If it doesn't exist, clone the repository
                        sh "git clone ${repoUrl}"
                    }
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    def imageTag = "akashgupta0408/weather-app:${env.BUILD_NUMBER}"
                    dir('CICD_Project')
                    sh 'ls -l'
                    sh "docker build -t ${imageTag} ."
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
                    sh "sed -i 's|image: akashgupta0408/weather-app:.*|image: ${imageTag}|g' deployment.yaml"
                    sh 'kubectl apply -f deploy.yaml'
                    sh 'kubectl apply -f service.yaml'
                    // Rollout the deployment
                    sh 'kubectl rollout status deployment/weather-app'
                }
            }
        }
    }
}
