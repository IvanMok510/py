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
                // For a simple hello world, this could just execute the script
                sh 'python3 app.py & sleep 5; curl http://localhost:8080; kill %1'  // Runs briefly and tests output
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
