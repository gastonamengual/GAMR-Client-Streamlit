# GAMR MLOps Project

This repo is part of the GAMR MLOps project, designed to showcase a flexible and scalable MLOps architecture. By integrating multiple clients and model registries, it simulates real-world industry scenarios where different components need to work together seamlessly. The goal is to demonstrate how a well-structured, decoupled system can make AI deployments more efficient, adaptable, and easy to maintain.

# Client Application

This repository contains the client application of the project. The client is built using Streamlit and interacts with a backend service to support both image classification and iris flower recognition.

## Architecture Overview
The client is part of a layered MLOps architecture:
- **Client:** Streamlit-based UI for user interaction.
- **Backend:** FastAPI service handling request validation and authentication, hosted both in Render as a Docker Image and on Vercel.
- **Model Registry:**
  - Hugging Face model for image classification.
  - MLFlow model hosted on Render in a Docker container for iris classification.

## Usage

1. Open the app in [https://gamr-image-recognition.streamlit.app](https://gamr-image-recognition.streamlit.app).

2. Chose either object detection or flower classification.

3. View predictions and results in real-time.

- **For image classification:** Upload an image, and the model will return the predicted class.
- **For iris classification:** Input sepal/petal measurements, and the model will predict the iris species.

## Deployment
This client can be deployed on platforms like Streamlit Sharing or a cloud provider supporting Python web applications.

## WIP and Future Enhancements
- 100% test coverage.
- Improved UI/UX for better interaction.
- Enhanced authentication and user management.

---

Feel free to suggest improvements!
