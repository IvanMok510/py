pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject() {
                            // Start an OpenShift build using the app's BuildConfig
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
                    pip3 install -r requirements.txt  # Install Flask (assumes requirements.txt has 'flask')
                    python3 app.py & sleep 5
                    curl http://localhost:8080
                    kill %1
                '''
            }
        }

        stage('Deploy') {
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject() {
                            // Roll out the latest deployment
                            openshift.deploy("hello-appp")
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
