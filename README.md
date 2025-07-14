# MusicApp

A Flask-based service that generates GLSL shader-based music visualizer videos using OpenAI and uploads them to Google Drive.

## Overview

📺DAIM –

It is a music production platform **_DAIM_** 's AI functions allow even those with no knowledge of music production to create music intuitively.

In order to avoid the mass production of uniform content, which is the fate of AI, **_DAIM_** will provide collaborative production tools with professional DJs and singers, creating a content environment that combines the efficiency that is AI's greatest feature with the originality that humans create.

In addition, the completed songs will be managed on the blockchain , including copyright, master rights, and portrait rights, as well as usage history such as the number of downloads and plays .

artists around the world to run AI generation workflows in real time, instantly accessible high-performance GPUs are essential. AI -based music production activities are carried out on the "JANCTION" chain, a low-cost, high-speed GPU cloud , reducing the cost of processing AI development data.

The completed song will be turned into a music video by a video creator, and the content will be managed by "JANCTION x IPFS".

**_DAIM will_** also handle distribution.

The completed content will be managed by JANCTION x IPFS, played on **_MyTube (tentative name) ,_** and sold for a fee on the newly constructed Web 3.0 audition platform **_DeXus ._**

DeXus allows artists **_and_** fans to interact directly and sell content created on **_DAIM directly to fans._**

🔗Key Features

- **_Automatic music generation function :_**　Users simply input natural language following the guidance.

The music is automatically generated .

- **_Collaboration features :_**　To polish the automatically generated content, users can apply for collaboration. If someone agrees to collaborate, they will be provided with real-time access and editing rights to the music files, allowing multiple people to edit the content simultaneously .
- **_Content storage function:_** Completed content is stored safely and inexpensively on JANCTION x IPFS.
- **_Content management features :_**　Completed content will be managed on the blockchain.
- **_Content sales features :_**　Content managed by blockchain can be sold within the DeXus platform . Artists can freely decide the selling price of their content.
- **_Content Rating Features :_**　You can add comments to the content .

💡Use Cases

- Secure archiving and streaming of premium video content.
- Monetization through token rewards and affiliate linked video commerce.
- Integration with virtual influencers and AI-generated media.
- A platform shift for creators restricted by centralized platforms.

🧩System Architecture

- **_Frontend:_** A web interface for users and creators with login, video upload, search and playback functionality.
- **_Backend:_** The IPFS Gateway handles video storage, encryption, access control, and interaction with the JANCTION blockchain.
- **_Cache Management:_** AI-based CDN optimization ensures smooth video playback without excessive costs.

🚀Development Roadmap  
Phase 1 – Basic Frontend (February – April)

- Creator Video Upload
- Video Streaming and Sharing
- User Registration and Social Login
- Search & Recommendation Engine

Phase 2 – IPFS Gateway (March to July)

- Distributed Storage and Search
- Blockchain transaction log via JANCTION node
- Secure encryption/decryption support

Phase 3 – Cash Management (April – August)

- Real-time access-based caching
- AI-based content preloading for trend optimization

🔧Future Scope

- Mobile app development for Android/iOS
- JCP-based Pay-per-view integration
- Video shopping and affiliate e-commerce features

If you're interested in building a censorship-resistant, creator-first video platform, we welcome submissions and feedback from developers, creators, and decentralization advocates.


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
