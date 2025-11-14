pipeline {
    agent any
    
    stages {
        stage('Verify Environment') {
            steps {
                bat '''
                    echo Verifying Minikube and Kubernetes...
                    minikube status && (
                        echo Minikube is running
                    ) || (
                        echo Starting Minikube...
                        minikube start --driver=docker
                    )
                    minikube kubectl -- cluster-info
                '''
            }
        }
        
        stage('Build and Deploy') {
            steps {
                bat '''
                    echo Building Docker image...
                    minikube docker-env | call
                    docker build -t hello-app:latest .
                    
                    echo Deploying to Kubernetes...
                    minikube kubectl -- apply -f hello-app-deployment.yaml
                    
                    echo Waiting for deployment to be ready...
                    minikube kubectl -- rollout status deployment/hello-app-deployment --timeout=180s
                    
                    echo Deployment successful!
                    minikube service hello-app-service --url
                '''
            }
        }
    }
    
    post {
        always {
            bat '''
                echo Performing cleanup...
                minikube kubectl -- delete -f hello-app-deployment.yaml 2>nul || echo "Cleanup done"
            '''
        }
    }
}