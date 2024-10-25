pipeline {
    agent any
    environment {
        DOCKER_CREDENTIALS_ID = 'docker-credentials'
        IMAGE_TAG = "akashgupta0408/weather-app:${env.BUILD_NUMBER}"
        EMAIL_RECIPIENTS = 'akashguptaking04@gmail.com' 
    }
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
                    def imageTag = "akashgupta0408/weather-app"
                    // Point to the correct directory where the Dockerfile is located
                    sh "docker build -t ${IMAGE_TAG} ."
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                   withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                        sh "docker push ${IMAGE_TAG}"
                    }
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                script {
             sh 'kubectl apply -f kubernetes/deploy.yml'
            // Update the deployment with the new image
            sh "kubectl set image deployment/weather-app weather-app=${IMAGE_TAG}"
            sh 'kubectl config use-context kind-kind'
            sh 'kubectl apply -f kubernetes/service.yml'
            // Rollout the deployment
            sh 'kubectl rollout status deployment/weather-app'
            sh 'sudo -u jenkins kubectl port-forward svc/weather-app 31224:80 --address 0.0.0.0 &'
            echo "App Accessible on <VM-ip:31224>"
        }
            }
        }
        stage('Monitoring') {
            steps {
                script {
            sh 'kubectl apply -f kubernetes/prometheusService.yml'
            sh 'kubectl apply -f kubernetes/grafanaService.yml'
            sh 'sudo -u jenkins kubectl port-forward svc/prometheus 30000:9090 --address 0.0.0.0 -n monitoring &'
            sh 'sudo -u jenkins kubectl port-forward svc/grafana 30001:3000 --address 0.0.0.0 -n monitoring &'
            echo "Promotheus Accessible on <VM-ip:30000>"
            echo "Grafana Accessible on <VM-ip:30001>"
        }
            }
        }
    }
        post {
        success {
            script {
                emailext (
                    subject: "Build Succeeded: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    body: """
                        Build succeeded for ${env.JOB_NAME} - ${env.BUILD_NUMBER} \n
                        Check console output at ${env.BUILD_URL} to view the results.
                    """,
                    to: EMAIL_RECIPIENTS
                )
            }
        }
        failure {
            script {
                emailext (
                    subject: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    body: """
                        Build failed for ${env.JOB_NAME} - ${env.BUILD_NUMBER} \n
                        Check console output at ${env.BUILD_URL} to view the results.
                    """,
                    to: EMAIL_RECIPIENTS
                )
            }
        }
    }
}

