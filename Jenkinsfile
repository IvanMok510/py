pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject() {
                            openshift.startBuild("hello-appp", "--wait=true")
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
                            def dc = openshift.selector('dc', 'hello-appp')
                            dc.rollout().latest()  // Triggers the rollout
                            timeout(10) {  // Waits up to 10 minutes
                                dc.rollout().status()  // Monitors rollout status until ready
                            }
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
