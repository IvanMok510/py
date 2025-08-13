pipeline {
    agent any
    parameters {
        string(name: 'APP_NAME', defaultValue: 'new-app')
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject() {
                            echo "Starting build for ${params.APP_NAME}..."
                            openshift.startBuild("${params.APP_NAME}", "--wait=true")
                            echo "Build completed."
                        }
                    }
                }
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                    python3 app.py & 
                    for i in {1..30}; do curl -f http://localhost:8080 && break || sleep 1; done
                    kill %1 || true
                    deactivate
                    rm -rf venv
                '''
            }
        }
        stage('Deploy') {
            steps {
                echo "Starting deploy for ${params.APP_NAME}..."
                script {
                    openshift.withCluster() {
                        openshift.withProject() {
                            openshift.deploy(deploymentConfig: "${params.APP_NAME}")
                            echo "Deploy completed."
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            echo 'Pipeline completed.'
        }
        success {
            echo 'All stages successful!'
        }
        failure {
            echo 'Pipeline failed. Check logs.'
        }
    }
}
