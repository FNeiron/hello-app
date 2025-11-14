pipeline {
    agent any
    
    stages {
        stage('Start Minikube') {
            steps {
                script {
                    // Проверяем статус minikube и запускаем если нужно
                    def status = bat(
                        script: 'minikube status',
                        returnStdout: true,
                        returnStatus: true
                    )
                    
                    if (status != 0) {
                        echo "Minikube is not running. Starting minikube..."
                        bat 'minikube start --driver=docker --force'
                    } else {
                        echo "Minikube is already running"
                    }
                    
                    // Ждем пока minikube полностью запустится
                    bat 'minikube status --wait=true'
                }
            }
        }
        
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        
        stage('Verify Kubernetes Access') {
            steps {
                bat '''
                    echo Verifying Kubernetes cluster...
                    minikube kubectl -- get nodes
                    minikube kubectl -- cluster-info
                '''
            }
        }
        
        stage('Deploy Application') {
            steps {
                bat '''
                    echo Deploying hello-app...
                    minikube kubectl -- apply -f hello-app-deployment.yaml
                '''
            }
        }
        
        stage('Wait for Deployment') {
            steps {
                bat '''
                    echo Waiting for pods to be ready...
                    timeout /t 30 /nobreak
                    minikube kubectl -- get pods -w
                '''
            }
        }
        
        stage('Verify Deployment') {
            steps {
                bat '''
                    echo Checking deployment status...
                    minikube kubectl -- get all
                    minikube kubectl -- logs -l app=hello-app --tail=5
                '''
            }
        }
    }
    
    post {
        always {
            echo '=== Pipeline Execution Completed ==='
            bat 'minikube kubectl -- get pods,services,deployments 2>nul || echo Cannot get Kubernetes resources'
        }
        success {
            echo '✅ SUCCESS: Application deployed successfully!'
            bat 'minikube service list | findstr hello || echo Hello service not found'
        }
        failure {
            echo '❌ FAILED: Pipeline execution failed'
        }
    }
}