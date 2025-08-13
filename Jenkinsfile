podTemplate(
    label: 'python-pod',
    containers: [
        containerTemplate(
            name: 'python',
            image: 'python:3.12-slim',
            command: 'cat',
            ttyEnabled: true
        )
    ]
) {
    pipeline {
        agent none
        environment {
            APP_NAME = 'python-app'
            GIT_REPO = 'https://github.com/IvanMok510/py.git'
            GIT_BRANCH = 'main'
            ARTIFACT_FOLDER = 'target'
            PORT = 8080
        }
        stages {
            stage('Get Latest Code') {
                agent { label 'python-pod' }
                steps {
                    git branch: "${GIT_BRANCH}", url: "${GIT_REPO}"
                }
            }
            stage('Install Dependencies') {
                agent { label 'python-pod' }
                steps {
                    container('python') {
                        sh '''
                        python -m venv venv
                        . venv/bin/activate
                        pip install -r requirements.txt || echo "No requirements.txt, skipping"
                        deactivate
                        '''
                    }
                }
            }
            stage('Run Tests') {
                agent { label 'python-pod' }
                steps {
                    container('python') {
                        sh '''
                        . venv/bin/activate
                        pytest --junit-xml=test-results.xml || true
                        deactivate
                        '''
                    }
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
            stage('Store Artifact') {
                agent { label 'python-pod' }
                steps {
                    script {
                        def safeBuildName = "${APP_NAME}_${BUILD_NUMBER}"
                        sh "mkdir -p ${ARTIFACT_FOLDER}"
                        sh "tar -czvf ${ARTIFACT_FOLDER}/${safeBuildName}.tar.gz ."
                        archiveArtifacts artifacts: "${ARTIFACT_FOLDER}/${safeBuildName}.tar.gz"
                    }
                }
            }
            stage('Create Image Builder') {
                agent none
                when {
                    expression {
                        openshift.withCluster() {
                            openshift.withProject('mkn022-dev') {
                                return !openshift.selector("bc", "${APP_NAME}").exists()
                            }
                        }
                    }
                }
                steps {
                    script {
                        openshift.withCluster() {
                            openshift.withProject('mkn022-dev') {
                                openshift.newBuild("--name=${APP_NAME}", "--image-stream=openshift/python:3.12-ubi8", "--binary=true")
                            }
                        }
                    }
                }
            }
            stage('Build Image') {
                agent none
                steps {
                    script {
                        openshift.withCluster() {
                            openshift.withProject('mkn022-dev') {
                                def build = openshift.selector("bc", "${APP_NAME}").startBuild("--from-archive=${ARTIFACT_FOLDER}/${APP_NAME}_${BUILD_NUMBER}.tar.gz", "--wait=true")
                                build.untilEach {
                                    def status = it.object().status.status
                                    echo "Build status: ${status}"
                                    return status == "Complete" || status == "Failed" || status == "Cancelled"
                                }
                                if (build.object().status.status != "Complete") {
                                    error "Build failed with status: ${build.object().status.status}"
                                }
                            }
                        }
                    }
                }
            }
            stage('Deploy') {
                agent none
                steps {
                    script {
                        openshift.withCluster() {
                            openshift.withProject('mkn022-dev') {
                                if (!openshift.selector('dc', "${APP_NAME}").exists()) {
                                    openshift.newApp("${APP_NAME}:latest").narrow("svc").expose("--port=${PORT}")
                                }
                                def dc = openshift.selector("dc", "${APP_NAME}")
                                dc.rollout().latest()
                                dc.rollout().status()
                                echo "Application URL: ${openshift.selector('route', '${APP_NAME}').object().spec.host}"
                            }
                        }
                    }
                }
            }
        }
    }
}
