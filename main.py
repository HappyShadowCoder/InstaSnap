# main.py (Corrected)
from flask import Flask, render_template, request
import uuid
from werkzeug.utils import secure_filename
import os
import subprocess
import threading

UPLOAD_FOLDER = 'user_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def run_generate_process():
    subprocess.Popen(['python3', 'generate_process.py'])

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/create", methods=["GET", "POST"])
def create():
    myid = uuid.uuid1()
    if request.method == "POST":
        rec_id = request.form.get("uuid")
        desc = request.form.get("text")
        current_upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], rec_id)
        os.makedirs(current_upload_dir, exist_ok=True)

        input_files = []
        for key, value in request.files.items():
            file = request.files[key]
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_upload_dir, filename))
                input_files.append(filename)

        with open(os.path.join(current_upload_dir, "desc.txt"), "w") as f:
            f.write(desc)

        with open(os.path.join(current_upload_dir, "input.txt"), "w") as f:
            for fl in input_files:
                f.write(f"duration 2\nfile '{fl}'\n")
            # Repeat last file (optional, improves duration reliability)
            if input_files:
                f.write(f"file '{input_files[-1]}'\n")

    return render_template("create.html", myid=myid)


@app.route("/gallery")
def gallery():
    reel_dir = "static/reels"
    all_files = os.listdir(reel_dir)
    reels = []
    for file in all_files:
        full_path = os.path.join(reel_dir, file)
        if file.endswith(".mp4") and os.path.getsize(full_path) > 0:
            reels.append(file)
    reels.sort(key=lambda f: os.path.getmtime(os.path.join(reel_dir, f)), reverse=True)
    return render_template("gallery.html", reels=reels)


if __name__ == "__main__":
    # Start the generate_process.py in a background thread
    threading.Thread(target=run_generate_process, daemon=True).start()

    # Now run your Flask app
    app.run(debug=True)