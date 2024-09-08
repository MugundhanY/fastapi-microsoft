# Microsoft TTS FastAPI Service

This repository contains a FastAPI application for generating text-to-speech (TTS) audio using Microsoft Edge TTS. It also includes an endpoint to retrieve available voices.

## Features

- **Text-to-Speech (TTS)**: Convert text into speech using Microsoft Edge TTS.
- **Voice List**: Retrieve a list of available voices and filter by name or locale.

## Getting Started

### Prerequisites

- Python 3.7 or later
- `pip` (Python package installer)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/microsoft-tts-fastapi.git
   cd microsoft-tts-fastapi
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Running Locally

1. Start the FastAPI application using `uvicorn`:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. The application will be accessible at `http://localhost:8000`.

### API Endpoints

#### 1. **Text-to-Speech (TTS)**

- **Endpoint**: `POST /tts`
- **Request Body** (JSON):

   ```json
   {
     "text": "Hello, how are you?",
     "voice": "en-US - (Female)",
     "rate": 10,
     "pitch": 5
   }
   ```

- **Response**: Audio file in MP3 format.

#### 2. **Available Voices**

- **Endpoint**: `GET /voices`
- **Query Parameters**: `query` (string for filtering by name or locale)
- **Response**: List of available voices.

### Deployment

To deploy the application on Render.com:

1. Create a `render.yaml` file (or use a `Procfile`):

   ```yaml
   services:
     - type: web
       name: microsoft-tts-service
       env: python
       buildCommand: "pip install -r requirements.txt"
       startCommand: "uvicorn main:app --host 0.0.0.0 --port 10000"
   ```

2. Push the code to your Git repository.

3. Connect your repository to Render.com and deploy the service.

### Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Microsoft Edge TTS](https://www.microsoft.com/en-us/edge/features)

