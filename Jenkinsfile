    pipeline {
      agent {
        kubernetes {
          yaml """
            apiVersion: v1
            kind: Pod
            metadata:
              labels:
                some-label: jenkins
            spec:
              containers:
              - name: molecule
                image: retr0h/molecule
                command:
                - cat
                tty: true
          """
        }
      }
      options {
        ansiColor('xterm')
      }
      stages {
        stage('Run maven') {
          steps {
            container('molecule') {
              withCredentials([string(credentialsId: 'AWS_ACCESS_KEY', variable: 'AWS_ACCESS_KEY'),string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')]) {
                sh '''
                  export ANSIBLE_FORCE_COLOR=true
                  export PY_COLORS=1
                  export AWS_ACCESS_KEY=$AWS_ACCESS_KEY
                  export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                  export EC2_REGION=eu-west-2

                  pip install --user --upgrade molecule==2.20
                  pip install --user --upgrade pytest testinfra
                  pip install --user botocore boto boto3
                  sudo apk add openssh-client         

                  cd /tmp && git clone https://github.com/Hachebourin/molecule_ti.git
                  cd /tmp/molecule_ti/ && molecule test -s ti
                '''
              }
            }
          }
        }
      }
    }