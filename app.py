from flask import Flask, request, jsonify
from flask_cors import CORS

import config
from scripts.video_generator import generate_video
from scripts.drive_uploader import upload_to_drive

app = Flask(__name__)
CORS(app)

# Endpoint 1: Generate video
@app.route("/generate-video", methods=["POST"])
def generate_video_endpoint():
    try:
        data = request.get_json() or {}
    except Exception:
        data = {}

    # Default fallback values (can be overridden via JSON body)
    moods     = data.get("moods",    ["happy"])
    genres    = data.get("genres",   ["funk"])
    themes    = data.get("themes",   ["travel"])
    music_url = data.get(
        "music_url",
        "https://soundraw-api-storage.com/final_1d377b75-80eb-4564-a6a5-feaabea8a9e1.mp3"
    )

    payload = {
        "moods":     moods,
        "genres":    genres,
        "themes":    themes,
        "music_url": music_url
    }

    try:
        print("[DEBUG] Generating shader and rendering video...")
        path = generate_video(payload)
    except Exception as e:
        print(f"[ERROR] Video generation failed: {e}")
        return jsonify({"error": f"Video generation failed: {str(e)}"}), 500

    return jsonify({
        "message":   "Shader video generated successfully",
        "videoPath": path
    }), 200

# Endpoint 2: Upload video
@app.route("/upload-video", methods=["POST"])
def upload_video_endpoint():
    try:
        print("[DEBUG] Uploading video to Google Drive...")
        file_id, drive_url = upload_to_drive()
    except Exception as e:
        print(f"[ERROR] Drive upload failed: {e}")
        return jsonify({"error": f"Drive upload failed: {str(e)}"}), 500

    return jsonify({
        "message":       "Video uploaded successfully",
        "videoDriveUrl": drive_url
    }), 200

if __name__ == "__main__":
    app.run(port=5000)
