# Career GPS

Your personal AI mentor to help you navigate your career journey


## Overview

Career GPS is a Streamlit-powered application designed to provide personalized career roadmaps. It leverages an AI model to generate tailored learning plans based on a user's current skills and desired career goals. To ensure the accuracy and trustworthiness of learning resources, the application incorporates a Retrieval-Augmented Generation (RAG) approach using web search capabilities. Additionally, it offers a progress tracking dashboard where users can manage their weekly goals and visualize their advancements.

## Features

* **Personalized Career Roadmap Generation**: Users can input their existing skills and desired career goals to receive a customized weekly learning roadmap.
* **AI-Powered Guidance**: Utilizes the Mistral-7B Instruct model via the OpenRouter API for roadmap generation. This model is specifically engineered through prompt engineering to act as a friendly and professional career roadmap mentor.
* **RAG for Trusted Resources**: Integrates the Serper.dev API for web search, enabling the AI to provide verified and relevant learning resources and links, preventing hallucination.
* **Progress Tracking Dashboard**: A dedicated dashboard allows users to:
    * Mark weekly goals as completed.
    * Add and edit their weekly goals.
    * Receive feedback on their weekly progress.
* **Interactive Visualizations**: Progress is visualized through a bar chart depicting weekly completion percentages and a pie chart showing overall progress.
* **User Authentication**: Secure user registration and login system.
* **Flexible Input**: Users can provide their background information by typing it manually or by uploading their resume (PDF or TXT formats supported).

## Installation

To get Career GPS up and running on your local machine, follow these steps:

## Prerequisites

* Python 3.8+
* `pip` (Python package installer)

## Environment Variables

Before running the application, you need to set up your API keys. Create a `.env` file in the root directory of your project and add the following:

    OPENROUTER_API_KEY="your_openrouter_api_key_here"
    SERPER_API_KEY="your_serper_api_key_here"

## Install Dependencies

Navigate to the project's root directory in your terminal and use the following command to install the required packages:

    pip install -r requirements.txt

## Usage

To start the Career GPS application, run the following command in your terminal from the project's root directory:

    streamlit run Main.py

## Workflow:
**1) Get Started:**
Click the "Get Started" button on the main page.

**2) Login/Register:** You will be redirected to the authentication page. Choose to "Login" if you have an existing account or "Register" to create a new one.

**3) Generate Roadmap:** After logging in, navigate to the "Generate Roadmap" page.

  ***Step 1:*** Tell us about your background: Enter your current skills, past courses, or projects manually, or upload your resume (PDF or TXT).

  ***Step 2:*** Choose your career goal. Input your desired career and click "Generate My Roadmap".

**4) Track Progress:** Access the "Track My Progress" dashboard to view and update your weekly goals. Mark tasks as completed, add new goals, and observe your progress through the interactive charts.

## Project Structure

    ├── Main.py
    ├── utils.py
    ├── db.py
    ├── requirements.txt
    └── pages/
        ├── auth.py
        ├── Generate_Roadmap.py
        ├── home.py
        └── progress_tracker.py

* **Main.py:** The entry point of the Streamlit application.
* **utils.py:** Contains utility functions for interacting with the AI model, performing web searches, and extracting topics.
* **db.py:** Handles database operations for user management and progress tracking using SQLite3.
* **requirements.txt:** Lists all Python dependencies required for the project.
* **pages/:** Directory containing separate Streamlit pages for better navigation.
    * **auth.py:** Manages user login and registration.
    * **Generate_Roadmap.py:** Interface for users to input their information and generate a career roadmap.
    * **home.py:** The welcome page displayed after a successful login.
    * **progress_tracker.py:** The dashboard for tracking and managing weekly career progress.
