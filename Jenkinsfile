pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/your/repo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t your-dockerhub/hello-app:latest .'
            }
        }

        stage('Push Image') {
            steps {
                sh '''
                    docker push your-dockerhub/hello-app:latest
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f hello-app-deployment.yaml
                '''
            }
        }
    }
}
