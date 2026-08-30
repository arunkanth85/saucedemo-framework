pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
               bat 'C:\\Users\\arun1\\AppData\\Local\\Programs\\Python\\Python310\\python.exe -m venv venv'
                bat '.\\venv\\Scripts\\pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                // Note: Jenkins agents have no display, so conftest.py's
                // --headless=new line must be uncommented for this to work.
                bat '.\\venv\\Scripts\\pytest'
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