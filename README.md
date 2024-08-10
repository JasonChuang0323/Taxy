# Taxy


# Taxy

## Overview

Taxy is a simple web application built with Python. It includes an API endpoint that responds to greeting requests. This document provides instructions for running the application and testing the API.

## Running the Application

To start the application, use the following command:

```sh
python run.py

This will launch the server on http://127.0.0.1:5000.


Send a Greeting
To send a POST request to the /api/greet endpoint with a name, use the following curl command:

curl http://127.0.0.1:5000/api/greet -H "Content-Type: application/json" -d '{"name": "Stranger"}'


Access the Home Page
To make a GET request to the root URL, use:

curl http://127.0.0.1:5000/

#Dependencies
Ensure you have the required dependencies installed. If you're using requirements.txt, you can install them with:

pip install -r requirements.txt
