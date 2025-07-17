from flask import Flask, request, jsonify, send_file
import yt_dlp, os, uuid

app = Flask(__name__)
os.makedirs("downloads", exist_ok=True)

@app.route("/download", methods=["POST"])
def download_audio():
    data = request.get_json()
    url = data.get("url")
    fmt = data.get("format", "mp3")
    
    file_id = str(uuid.uuid4()) + "." + fmt
    path = os.path.join("downloads", file_id)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": path,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": fmt,
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify(success=True, file=f"/files/{file_id}")
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route("/files/<filename>")
def serve_file(filename):
    return send_file(os.path.join("downloads", filename), as_attachment=True)

# ✅ Render এ কাজ করার জন্য এটা অবশ্যই দরকার
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
