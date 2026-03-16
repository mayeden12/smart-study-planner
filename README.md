<div align="center">

  # Smart Study Planner
  
  <p><strong>Your personal learning assistant, powered by local AI.</strong></p>

</div>

---

## About The Project

Tired of managing your study tasks across scattered notebooks and apps? **Smart Study Planner** is a full-stack solution designed to centralize your learning journey. 

Organize your subjects, track deadlines, and generate AI-driven "study hacks" to help you learn more efficiently—all running locally and securely on your own machine without relying on external cloud APIs.

### Key Capabilities

*   **Rapid AI Insights:** Get focused learning strategies for any topic using a locally hosted LLM.
*   **Visual Daily Schedule:** View your daily tasks and track progress effortlessly.
*   **Unified Learning Hub:** Keep all your subjects, notes, and deadlines in one organized space.
*   **Progress Tracking:** Stay motivated with visual progress indicators.
*   **One-Click Deployment:** Spin up the entire system easily using Docker Compose.

---

## Quick Start (Recommended)

The easiest and most reliable way to run the project is via Docker.

1.  **Ensure Docker is installed** on your machine.
2.  **Clone the repository** and navigate to the folder:
    ```bash
    git clone <YOUR_REPO_URL>
    cd smart-study-planner
    ```
3.  **Start the services:**
    ```bash
    docker-compose up --build
    ```
    *(This will build and start the Frontend, Backend, and Ollama containers).*

4.  **Download the AI Model (One-time setup):**
    Open a **new terminal window** and run:
    ```bash
    docker exec -it ollama ollama pull tinyllama
    ```

5.  **You're all set! Access the app:**
    *   **User Interface:** http://localhost:8501
    *   **API Documentation:** http://localhost:8000/docs

---

## Local Development Setup

<details>
  <summary>Click here for non-Docker setup instructions</summary>

  ### 1. Prerequisites
  *   Python 3.9+
  *   `uv` package manager (`pip install uv`)
  *   Ollama installed and running locally.

  ### 2. Environment Setup
  ```bash
  # Create and activate a virtual environment
  uv venv
  source .venv/bin/activate  # macOS/Linux
  # .venv\Scripts\Activate.ps1 # Windows

  # Install dependencies
  uv pip install -r requirements.txt

  # Download the AI model
  ollama pull tinyllama
  ```

  ### 3. Running the App
  You will need two separate terminal windows (with the virtual environment activated in both).

  **Terminal 1 (Backend):**
  ```bash
  # Set Ollama environment variable
  $env:OLLAMA_HOST="http://localhost:11434" # Windows
  # export OLLAMA_HOST=http://localhost:11434  # macOS/Linux

  # Start the FastAPI server
  uvicorn app.main:app --reload
  ```

  **Terminal 2 (Frontend):**
  ```bash
  streamlit run frontend/streamlit_app.py
  ```
</details>

---

## API Endpoints

| Method | Endpoint              | Description                                    |
|--------|-----------------------|------------------------------------------------|
| GET    | `/topics`             | Retrieves all study topics.                    |
| POST   | `/topics`             | Creates a new study topic.                     |
| PATCH  | `/topics/{id}`        | Updates a topic (e.g., status, favorite).      |
| DELETE | `/topics/{id}`        | Deletes a study topic.                         |
| POST   | `/topics/{id}/hack`   | Generates an AI study hack for a topic.        |

---

## Testing

To run the test suite, ensure your virtual environment is active and execute:
```bash
pytest
```

---

## 🤝 Contributing & License

Contributions, issues, and feature requests are welcome! 
This project is licensed under the MIT License.