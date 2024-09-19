**MLOps Project with MLflow, Docker, and GitHub Actions**

**Project Overview**

This repository demonstrates a complete MLOps pipeline for a simple regression model using MLflow, Docker, and GitHub Actions. The project includes:

-   **Model Training and Logging**: MLflow is used for model tracking and logging.
-   **Docker**: Containerization of the application and environment.
-   **GitHub Actions**: CI/CD pipeline for automated build, push, and deployment.

**Project Structure**

·         `**docker-compose.yml**`: Defines services for MLflow and the regression model, including image names and commands. This file ensures that the containers are set up with the correct configurations and dependencies.

·         `**Dockerfile**`: Contains instructions to build a Docker image for the project, including the setup of the environment, installation of dependencies, and configuration of the entry point. This file creates a reproducible environment for running the application.

·         `**requirements.txt**`: Lists all the Python libraries required for the project, ensuring that the environment has the necessary packages for running the regression model and MLflow. This file is used during the Docker image build process to install dependencies.

·         `**main.py**`: Implements the regression model and includes code for training, evaluation, and MLflow integration. This script is the main application logic and interacts with MLflow for experiment tracking and model logging.

**How It Works**

1.  **Local Setup**:

-   Ensure Docker is installed on your machine.
-   Use Docker Compose to build and run the services locally.
-   Access the MLflow UI at http://localhost:5000 to view logged experiments and models.

2.  **Continuous Integration and Deployment**:

-   The GitHub Actions workflow (ci-cd.yml) automates the process:

-   **Build**: Creates a Docker image for the application.
-   **Push**: Pushes the Docker image to Docker Hub.
-   **Run**: Uses Docker Compose to deploy the services, including MLflow and the application.

**Running the Project Locally**

1.  Clone the repository:

git clone https://github.com/mugunthragav/diab\_mlops.git

cd https://github.com/mugunthragav/diab\_mlops.git

2.  Build and run the services using Docker Compose:

docker-compose up --build

3.  Access the MLflow UI at http://localhost:5000 to monitor experiments and models.

**GitHub Actions Workflow**

-   **Trigger**: The workflow is triggered on pushes to the main branch and pulls requests.
-   **Steps**:

-   Checkout code
-   Set up Docker Buildx
-   Log in to Docker Hub
-   Build and push Docker image
-   Run Docker Compose to deploy the application and MLflow services

**Troubleshooting**

-   **MLflow UI Not Accessible**: Ensure Docker containers are running and check the ports used in docker-compose.yml.
-   **Build or Push Errors**: Verify Docker Hub credentials and repository names in the GitHub Actions workflow.

**Future Improvements**

·  **Artifact Storage**: Store artifacts, logs, and metrics in a cloud storage solution (e.g., AWS S3) for better accessibility and management.

·  **Data Access via REST API**: Develop a REST API to access data and model predictions, facilitating integration with other applications.

·  **Model Serving**: Deploy the ML model as a web application to provide customers .

·  **Continuous Refinement and Updating**: Establish CI/CD practices to ensure the model is automatically refined, trained, and updated based on new data and performance metrics.

·         **Logging and Monitoring**

**Option 1: Implement with Various Tools**

For logging and monitoring, integrating **MLflow** is an effective way to log model metrics and parameters. To visualize these metrics and gain insights into model performance, set up **Prometheus** to get data from your application and use **Grafana** for dashboarding and alerting.

**Option 2: Implement with Docker and Git**

Alternatively, you can achieve logging and monitoring through a Docker setup by extending your docker-compose.yml to include services for Prometheus and Grafana alongside your application. By creating a prometheus.yml configuration file that specifies the metrics to be logged and monitored, you can mount this file in your Docker container for Prometheus.

**Model Retraining and Versioning**

**Option 1: Implement with Various Tools**

To implement automatic model retraining, use **Prometheus** for monitoring performance metrics and set alerts in **Grafana** to notify you low performance of modeld. Additionally, employ **Great Expectations** to validate incoming data quality, triggering retraining when significant deviations are detected, with **Apache Airflow** managing and scheduling these workflows.

**Option 2: Implement with Docker and Git**

Alternatively, create a Docker-based solution with a Dockerfile specifying dependencies for the retraining environment. Automate the building and execution of the retraining script in your GitHub Actions workflow (.github/workflows/retrain.yml), while a docker-compose.yml file defines a dedicated service, ensuring consistent environment management across setups.
