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
                            sh 'git pull origin main'
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
                    dir('CICD_Project'){
                    sh 'ls -l'
                    sh "docker build -t ${imageTag} ."}
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
                    def nodePort = sh(script: "kubectl get svc weather-app -o jsonpath='{.spec.ports[0].nodePort}'", returnStdout: true).trim()
                    sh 'kubectl port-forward svc/weather-app ${nodePort}:80 --address 0.0.0.0'
                }
            }
        }
    }
}
