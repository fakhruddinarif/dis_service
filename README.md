# DIS Service

## Table of Contents
- [Introduction](#introduction)
- [Forking the Repository](#forking-the-repository)
- [Cloning the Repository](#cloning-the-repository)
- [Setting Up the Environment](#setting-up-the-environment)
- [Installing Dependencies](#installing-dependencies)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Contributing](#contributing)

## Introduction
This project is a FastAPI-based service for managing user registrations and logins. It uses Pydantic for data validation and MongoDB for data storage.

## Forking the Repository
1. Go to the [repository](https://github.com/fakhruddinarif/dis_service).
2. Click the `Fork` button in the top-right corner of the page.
3. Select your GitHub account to fork the repository.

## Cloning the Repository
1. Open your terminal.
2. Clone the forked repository to your local machine:
    ```sh
    git clone https://github.com/<your-username>/dis_service.git
    ```
3. Navigate to the project directory:
    ```sh
    cd dis_service
    ```

## Setting Up the Environment
1. Create a virtual environment:
    ```sh
    python -m venv .venv
    ```
2. Activate the virtual environment:
    - On Windows:
        ```sh
        .venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source .venv/bin/activate
        ```

## Installing Dependencies
1. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Application
1. Start the FastAPI application:
    ```sh
    uvicorn app.main:app --reload
    ```
2. Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the API documentation.

## Running Tests
1. Run the tests using `pytest`:
    ```sh
    pytest
    ```

## Contributing
1. Create a new branch for your feature or bugfix:
    ```sh
    git checkout -b feature/your-feature-name
    ```
2. Make your changes and commit them:
    ```sh
    git commit -m "Add your commit message"
    ```
3. Push your changes to your forked repository:
    ```sh
    git push origin feature/your-feature-name
    ```
4. Create a pull request from your forked repository to the main repository.