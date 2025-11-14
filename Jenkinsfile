pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/FNeiron/hello-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t neironx/hello-app:latest .'
            }
        }

        stage('Push Image') {
            steps {
                sh '''
                    docker push neironx/hello-app:latest
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
