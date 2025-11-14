pipeline {
    agent any
    
    stages {
        stage('Validate Environment') {
            steps {
                bat """
                    echo Validating environment...
                    minikube status || echo Minikube not running
                    minikube kubectl -- version --client || echo Minikube kubectl not available
                """
            }
        }
        
        stage('Ensure Minikube Running') {
            steps {
                script {
                    def minikubeStatus = bat(
                        script: 'minikube status',
                        returnStdout: true
                    ).trim()
                    
                    if (!minikubeStatus.contains("Running")) {
                        echo "Starting minikube..."
                        bat 'minikube start'
                    }
                }
            }
        }
        
        stage('Deploy Application') {
            steps {
                bat """
                    echo Deploying hello-app...
                    minikube kubectl -- apply -f hello-app-deployment.yaml
                """
            }
        }
        
        stage('Monitor Deployment') {
            steps {
                bat """
                    echo Monitoring deployment progress...
                    minikube kubectl -- get pods -w --timeout=60s
                    minikube kubectl -- get services
                """
            }
        }
    }
    
    post {
        always {
            echo '=== FINAL STATUS ==='
            bat 'minikube kubectl -- get all'
        }
        success {
            echo '✅ SUCCESS: Application deployed successfully!'
            bat 'minikube service list | findstr hello'
        }
        failure {
            echo '❌ FAILED: Deployment failed'
            bat 'minikube kubectl -- describe deployment hello-app-deployment || echo Cannot describe deployment'
            bat 'minikube kubectl -- get events --sort-by=.lastTimestamp || echo Cannot get events'
        }
    }
}