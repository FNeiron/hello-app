pipeline {
    agent any
    
    tools {
        jdk 'jdk11'
    }
    
    stages {
        stage('Check Windows Environment') {
            steps {
                bat 'systeminfo | findstr /B /C:"OS Name" /C:"OS Version"'
                bat 'kubectl version --client'
                bat 'minikube version'
            }
        }
        
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        
        stage('Deploy Application') {
            steps {
                bat '''
                    echo Deploying to Kubernetes...
                    kubectl apply -f hello-app-deployment.yaml
                    timeout /t 30 /nobreak
                    kubectl get pods -o wide
                '''
            }
        }
        
        stage('Wait for Pods') {
            steps {
                bat '''
                    echo Waiting for pods to be ready...
                    kubectl wait --for=condition=ready pod -l app=hello-app --timeout=180s
                    kubectl get pods
                '''
            }
        }
        
        stage('Verify Deployment') {
            steps {
                bat '''
                    echo Verifying deployment...
                    kubectl get deployment hello-app-deployment
                    kubectl get service hello-app-service
                '''
            }
        }
        
        stage('Access Application') {
            steps {
                bat '''
                    echo Testing application access...
                    minikube service list
                    kubectl port-forward service/hello-app-service 8080:80 &
                    timeout /t 5
                    curl http://localhost:8080
                    taskkill /f /im kubectl.exe
                '''
            }
        }
    }
    
    post {
        always {
            bat '''
                echo Collection final status...
                kubectl get all
            '''
        }
        success {
            echo '🎉 Pipeline executed successfully on Windows!'
        }
        failure {
            echo '❌ Pipeline failed'
        }
    }
}