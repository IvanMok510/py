pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject() {
                            echo "Starting build for hello-appp..."
                            openshift.startBuild("hello-appp", "--wait=true")
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
                    curl http://localhost:5000
                    kill %1 || true
                '''
            }
        }

        stage('Deploy') {
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject() {
                            echo "Starting deploy for hello-appp..."
                            def dc = openshift.selector('dc', 'hello-appp')
                            dc.rollout().latest()
                            timeout(10) {
                                dc.rollout().status()
                            }
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
    }
}
