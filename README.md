# Smart Meeting Summarizer (FastAPI + Streamlit)

A full-stack application that uses a local LLM to transform messy meeting notes into structured summaries.
- **Backend**: FastAPI microservice for AI processing.
- **Frontend**: Streamlit UI for easy text input and summary display.

---

## 🌟 New Features
- **🤖 AI-Powered Summarization**: Automatically generates a concise summary from raw text using `TinyLlama`.
- **📝 Action Item Extraction**: Identifies and lists tasks, assignees, and deadlines from the meeting notes.
- **🐳 Dockerized Architecture**: Seamless multi-container setup with Docker Compose.
---

## 📂 Project Structure



```text
MeetingSummarizer/
├── app/
│   ├── api/            # API endpoint for summarization
│   ├── core/           # AI summarization logic
│   └── schemas/        # Pydantic validation schemas
├── frontend/
│   ├── api_client.py   # API Communication Logic
│   └── streamlit_app.py# Streamlit UI
├── docker-compose.yml  # Multi-container orchestration
├── Dockerfile          # Backend containerization
└── requirements.txt
```

---

# 🚀 Getting Started

This project uses **uv** for environment management and dependency installation.

## 1. Create a uv virtual environment

From the project root:

```bash
uv venv
```

## 2. Activate the environment

**Windows (PowerShell):**
```bash
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

## 3. Install Dependencies

```bash
uv pip install -r requirements.txt
```

---

# 🖥️ Running the Application
## Prerequisites

1. Download and install Ollama from ollama.com
2. Installed on your system, uv (pip install uv)
3. Ensure the Ollama app is running, then pull the model:
```bash
ollama pull tinyllama
```
4. Install Dependencies - from project root
```bash
uv sync
```

## Step 1: Start the FastAPI Backend

### Set environment variable so the backend knows where Ollama is
```bash
export OLLAMA_HOST=http://localhost:11434  # macOS/Linux
$env:OLLAMA_HOST="http://localhost:11434" # Windows PowerShell
```

### Start the FastAPI server:

```bash
uv run uvicorn app.main:app --reload
```

The backend server runs on: **http://127.0.0.1:8000**

Swagger UI documentation: **http://127.0.0.1:8000/docs**

## Step 2: Start the Streamlit Frontend

In a **new terminal window** (with the virtual environment activated), run:

```bash
streamlit run frontend/streamlit_app.py
```

The Streamlit UI will open automatically in your browser at: **http://localhost:8501**

---

# 🎨 UI Overview

The Streamlit frontend provides a clean interface for summarizing your meeting notes.

## UI Features

1.  **📝 Input Area**: A large text area to paste your raw meeting notes or any other text.
2.  **✨ Generate Summary Button**: Kicks off the AI summarization process.
3.  **📄 AI-Generated Summary Display**: The structured summary, including action items and deadlines, is displayed neatly using Markdown.

---

# 🔌 API Overview

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/summarize` | Accepts raw text and returns an AI-generated summary. |
## Request Example
**POST** `/summarize`
```json
{
  "text": "The meeting was about the Q3 launch. Alice will handle the marketing slides by Friday. Bob is responsible for the final code review, due next Wednesday. We need to finalize the budget."
}
```

**DELETE** `/tasks/{id}`
```json
{
  "message": "Task 1 deleted successfully"
}
```

---

# 🧪 Running Tests

The project uses pytest + FastAPI's TestClient.

To run the test suite:

```bash
uv run pytest
```

---

# 🐳 Docker

The easiest way to run the entire application, including the AI engine and the database, is using Docker Compose. This ensures all services (Frontend, Backend, and Ollama) are correctly networked.
**Build the Docker image:**
```bash
docker-compose up --build
```

**Initialize the AI Engine**
In a new terminal, download the lightweight AI model:
```bash
docker exec -it ollama ollama pull tinyllama
```

### 📝 Docker Notes:
- Persistence: A Docker Volume named ollama_data is created to ensure your AI models stay saved even if the containers are stopped.
- Networking: Inside the Docker network, the Frontend communicates with the Backend using the hostname http://backend:8000.
---

# 📝 Notes

- Make sure the FastAPI backend is running before starting the Streamlit frontend

---

# 🛠️ Troubleshooting

**Cannot connect to API error in Streamlit:**
- Ensure the FastAPI server is running on http://127.0.0.1:8000
- Check that no firewall is blocking the connection

**Port already in use:**
- FastAPI default: 8000
- Streamlit default: 8501
- Use different ports if these are occupied

---

# 📚 Technology Stack

- **Backend**: FastAPI, Pydantic, Uvicorn
- **Frontend**: Streamlit
- **Testing**: pytest, TestClient
- **Environment**: uv (Python package manager)
- **Containerization**: Docker
- **AI Engine**: Ollama (Model: tinyllama)

# 📝 Performance Notes
Local AI: The AI model runs locally on your CPU. Ensure Docker is allocated at least 4GB of RAM for smooth performance.