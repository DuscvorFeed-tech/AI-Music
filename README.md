# MusicApp

A Flask-based service that generates GLSL shader-based music visualizer videos using OpenAI and uploads them to Google Drive.

## Overview

This application provides two endpoints:

1. **`POST /generate-video`**

   * Generates an abstract shader video synchronized to a provided audio URL.
   * Outputs a video file at `temp/generated_video.mp4`.
2. **`POST /upload-video`**

   * Uploads the generated video file to a specified Google Drive folder.
   * Returns a publicly shareable link.

## Prerequisites

* **Python 3.11+**
* Google Cloud Service Account with Drive API enabled
* OpenAI API key with access to GPT-4

## Setup and Installation

1. **Clone the repository**:

   ```bash
   git clone <your-repo-url>
   cd MusicApp
   ```

2. **Create and activate a virtual environment**:

   ```bash
   py -3.11 -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate    # macOS/Linux
   ```

3. **Install dependencies**:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Environment Configuration**:

   * Copy the example environment file and populate it with your secrets:

     ```bash
     copy .env.example .env     # Windows
     cp .env.example .env       # macOS/Linux
     ```
   * Edit **`.env`** and set:

     ```dotenv
     OPENAI_API_KEY=sk-...
     GOOGLE_SERVICE_ACCOUNT_FILE=service-account.json
     DRIVE_FOLDER_ID=your-folder-id
     ```
   * **Important**: Do **not** commit `.env` or your real keys to version control.

5. **Add Google Service Account Key**:

   * Download the JSON key for your service account and place it at the path specified by `GOOGLE_SERVICE_ACCOUNT_FILE` (default: `service-account.json`).
   * Ensure the Drive API is enabled for this service account.

## Running the Application

```bash
# With venv activated
python app.py
```

The service will run at `http://localhost:5000`.

### Generate Video

```bash
curl.exe -X POST http://localhost:5000/generate-video \
  -H "Content-Type: application/json" \
  -d '{
        "moods": ["happy"],
        "genres": ["funk"],
        "themes": ["travel"],
        "music_url": "https://soundraw-api-storage.com/final_1d377b75-80eb-4564-a6a5-feaabea8a9e1.mp3"
      }'
```

Response:

```json
{
  "message": "Shader video generated successfully",
  "videoPath": "temp/generated_video.mp4"
}
```

### Upload Video

```bash
curl.exe -X POST http://localhost:5000/upload-video
```

Response:

```json
{
  "message": "Video uploaded successfully",
  "videoDriveUrl": "https://drive.google.com/..."
}
```

## Suggested Repository Files

* **`.env.example`**: Template for environment variables
* **`.gitignore`**:

  ```gitignore
  venv/
  temp/
  .env
  service-account.json
  ```
* **`requirements.txt`**
* **`config.py`**
* **`app.py`**
* **`scripts/`** directory with `video_generator.py` and `drive_uploader.py`

## Next Steps Before Commit

* Ensure **`.gitignore`** is up-to-date to exclude sensitive files.
* Verify **`.env`** and **`service-account.json`** are not tracked by Git.
* Optionally, add tests for endpoint functionality.
* Consider adding a Dockerfile or CI pipeline configuration.

---

*Generated on: June 24, 2025*
