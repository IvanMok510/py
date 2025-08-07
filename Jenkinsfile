pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject() {
                            echo "Starting build for hello-app..."
                            openshift.startBuild("hello-app", "--wait=true")
                            echo "Build completed."
                        }
                    }
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests (e.g., run the script)...'
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                    python3 app.py & sleep 5
                    curl http://localhost:8080
                    kill %1 || true
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo "Starting deploy for hello-app..."
                sh '''
                    namespace=$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace)
                    oc rollout restart deployment/hello-app -n $namespace
                    oc rollout status deployment/hello-app -n $namespace --timeout=10m
                '''
                echo "Deploy completed."
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }
    }
}
