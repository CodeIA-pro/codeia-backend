# Django REST Framework with MongoDB Backend Project

## Overview

This project addresses the need for automatic documentation generation for backend development projects, specifically those built with Django. The proposal focuses on creating a tool that integrates with the GitHub API, allowing users to select a specific Django project and automatically generate reference guides. These technical guides aim to provide developers with a clear and quick understanding of how a particular API functions.

### Problem Statement

This project was initiated in response to three main issues:
1. **Lack of Documentation**: Often due to time constraints, developers do not document their projects adequately.
2. **Perception of Documentation**: Documentation is frequently viewed as a non-priority task, leading to its neglect within organizations.
3. **Organizational Culture**: Many organizations rely solely on developers' tacit knowledge without promoting the creation of technical documentation. This is risky as any developer might leave the project at any time.

By automating the documentation process, this project aims to improve the understanding and maintenance of APIs, thereby facilitating better project management and developer onboarding.

## Physical Architecture

The physical architecture of the project is designed to ensure optimal performance, scalability, and security. Below is a diagram illustrating the physical components and their interactions:

![System Architecture Diagram](https://firebasestorage.googleapis.com/v0/b/fir-dataapp-c6043.appspot.com/o/DIAGRAMA2.png?alt=media&token=2b1d1fbc-7a0c-4429-8df4-0a77f9242572)

## Project Structure

The project is structured as follows:
```
Root/
│
├── app/        # Contains settings and main configurations for Django REST Framework
│
├── codeia/     # General project structure including models and other core files
│
├── <filename>  # Files in the root act as domains for specific functionalities
│
└── manage.py   # Django's command-line utility for administrative tasks
```

## Installation and Setup

To run this project locally, follow these steps:
1. **Clone the Repository**:
    ```bash
    git clone <repository-url>
    ```

2. **Navigate to the Project Directory**:
    ```bash
    cd <project-directory>
    ```

3. **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    ```

4. **Activate the Virtual Environment**:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

5. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

6. **Run the Server**:
    ```bash
    python manage.py runserver
    ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes or improvements you would like to make.

## Support

For any questions or direct contact, please reach out to: `support@codeia.pro`
