# WebClusterBalancer

## Project Overview

**WebClusterBalancer** is a highly scalable and resilient web application architecture that leverages Docker containerization and Nginx as a reverse proxy load balancer. The system comprises three main components:

1. **Nginx Load Balancer**: A powerful reverse proxy server that acts as a single entry point for incoming client requests. It distributes the traffic across multiple application containers, ensuring high availability and load balancing.

2. **Python Web Application**: A Flask-based Python web application that exposes two endpoints:
   - `/`: Increments a global counter, saves it to a MySQL database, creates a session cookie with the internal IP address of the application container, records the access log with client IP, access time, and internal IP, and returns the internal IP address to the browser.
   - `/showcount`: Returns the current value of the global counter.

3. **MySQL Database**: A persistent MySQL database that stores the global counter value and access logs. The database data is persisted using Docker volumes, ensuring data integrity even after container restarts.

The architecture is designed to provide a scalable and fault-tolerant solution for web applications. The Nginx load balancer ensures that incoming traffic is distributed evenly across multiple application containers, improving overall performance and resilience. Additionally, the load balancer implements session stickiness using cookies, ensuring that subsequent requests from the same client are routed to the same application container for a period of 5 minutes, improving user experience and session management.

The application containers can be easily scaled up or down using a provided bash script, allowing for dynamic resource allocation based on demand. The integration with GitHub Actions and AWS Elastic Container Registry (ECR) enables automated Docker image builds and pushes to a private ECR repository upon code commits, facilitating continuous integration and deployment (CI/CD) workflows.

## Features

- **Load Balancing**: Nginx load balancer distributes incoming traffic across multiple application containers.
- **Session Stickiness**: Nginx uses cookies to maintain sticky sessions, ensuring that subsequent requests from the same client are routed to the same application container for a period of 5 minutes.
- **Reverse Proxy**: Nginx acts as a reverse proxy, providing a single entry point for client requests and forwarding them to the appropriate application containers.
- **Persistent Data**: The application logs and MySQL database data are persisted using Docker volumes, allowing data to be retained even after containers are stopped or restarted.
- **Scalability**: The application containers can be scaled up or down using a provided bash script.
- **Continuous Integration/Continuous Deployment (CI/CD)**: GitHub Actions workflow builds and pushes Docker images to AWS ECR upon code commits.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repo.git
    ```

2. Navigate to the project directory:

    ```bash
    cd your-repo
    ```

3. Create a `.env` file in the root directory with the following content:

    ```bash
    MYSQL_ROOT_PASSWORD=your_mysql_root_password
    ```

    Replace `your_mysql_root_password` with a desired password for the MySQL root user.

4. Build and start the Docker containers:

    ```bash
    docker-compose up -d --build
    ```

    This will build the Docker images and start the containers in detached mode.

5. Access the application at http://localhost.

## Usage

- To access the global counter, visit http://localhost/showcount.
- To increment the global counter and create a new access log entry, visit http://localhost/.
- The application logs can be found in the `python-app/logs` directory.
- The MySQL database data and logs are stored in the `db-data` and `db-logs` volumes, respectively.

## Scaling Containers

To scale the number of application containers, run the following script:

```bash
./scale_containers.sh [number_of_containers]
```

Replace [number_of_containers] with the desired number of application containers (e.g., 5).