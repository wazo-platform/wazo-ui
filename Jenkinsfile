pipeline {
  agent any
  environment {
    MAIL_RECIPIENTS = 'dev+tests-reports@wazo.community'
  }
  options {
    skipStagesAfterUnstable()
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '10'))
  }
  stages {
    stage('Debian build and deploy') {
      steps {
        build job: 'build-package-no-arch', parameters: [
          string(name: 'PACKAGE', value: "wazo-ui"),
          string(name: "BRANCH", value: "bullseye"),
          string(name: "DISTRIBUTION", value: "wazo-dev-wip-bullseye"),
        ]
      }
    }
    stage('Docker build') {
      steps {
        sh "sed -i 's/master.zip/bullseye.zip/g' requirements.txt"
        sh "docker build -t wazoplatform/wazo-ui:bullseye ."
        sh "sed -i 's/bullseye.zip/master.zip/g' requirements.txt"
      }
    }
    stage('Docker publish') {
      steps {
        sh "docker push wazoplatform/wazo-ui:bullseye"
      }
    }
  }
  post {
    failure {
      emailext to: "${MAIL_RECIPIENTS}", subject: '${DEFAULT_SUBJECT}', body: '${DEFAULT_CONTENT}'
    }
    fixed {
      emailext to: "${MAIL_RECIPIENTS}", subject: '${DEFAULT_SUBJECT}', body: '${DEFAULT_CONTENT}'
    }
  }
}
