pipeline {
    agent any
    
    environment {
        DOCKER_HOST = "tcp://localhost:2375"
    }
    
    stages {
        stage('Checkout') {
            steps {
                bat 'git --version'
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    // Используем локальный Docker daemon
                    docker.build("hello-app:${env.BUILD_ID}")
                }
            }
        }
        
        stage('Load Image to Minikube') {
            steps {
                script {
                    // Загружаем образ в Minikube
                    bat "minikube image load hello-app:${env.BUILD_ID}"
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Обновляем манифест с новым тегом образа
                    bat """
                    powershell -Command "(Get-Content hello-app-deployment.yaml) -replace 'hello-app:latest', 'hello-app:${env.BUILD_ID}' | Set-Content hello-app-deployment.yaml"
                    """
                    
                    // Применяем манифест в Kubernetes
                    bat "kubectl apply -f hello-app-deployment.yaml"
                    
                    // Ждем пока поды поднимутся
                    bat "kubectl rollout status deployment/hello-app-deployment --timeout=300s"
                }
            }
        }
        
        stage('Test Deployment') {
            steps {
                script {
                    // Получаем URL сервиса через Minikube
                    bat "minikube service hello-app-service --url"
                    
                    // Ждем немного и тестируем
                    bat "timeout /t 10"
                    bat "curl http://localhost:8080/health"
                }
            }
        }
    }
    
    post {
        always {
            // Очистка
            bat "kubectl delete -f hello-app-deployment.yaml || true"
        }
        success {
            echo 'Deployment completed successfully!'
        }
        failure {
            echo 'Deployment failed!'
        }
    }
}