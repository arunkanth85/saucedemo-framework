pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                // Pulls the latest code from your GitHub repo
                git branch: 'main', url: 'https://github.com/<your-username>/saucedemo-framework.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                // Note: Jenkins agents have no display, so conftest.py's
                // --headless=new line must be uncommented for this to work.
                sh './venv/bin/pytest'
            }
        }
    }

    post {
        always {
            // Makes the HTML report downloadable from the Jenkins build page
            archiveArtifacts artifacts: 'reports/report.html', allowEmptyArchive: true
        }
    }
}
