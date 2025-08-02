# **InstaSnap**

**AI Reel Generator** is an AI-powered web application that enables users to create short video reels by combining uploaded images with a custom text-to-speech voiceover. It features a **Flask** backend for handling requests and file uploads, and a background worker for intensive video/audio processing.

---

## **Features**

- **Web Interface**  
  A clean and simple UI built with Flask, Bootstrap, and Jinja2 templates. It includes a homepage, reel creation form, and a gallery for displaying completed reels.

- **Image and Text Uploads**  
  Users can upload multiple image files and provide a text description.

- **Asynchronous Processing**  
  The app uses a decoupled architecture:  
  - Flask server handles uploads and queues them  
  - A separate Python process handles video/audio generation in the background

- **Text-to-Speech Integration**  
  Converts the user’s text into a high-quality audio file using the **ElevenLabs API**.

- **FFmpeg Video Generation**  
  Uses **FFmpeg** to:
  - Stitch images together
  - Sync them with audio
  - Output vertical MP4 videos optimized for platforms like Instagram Reels

- **Dynamic Gallery**  
  A dynamic gallery (`gallery.html`) displays all successfully created reels from the `static/reels` directory.

---

## **Technologies Used**

- **Backend:** Python, Flask, Jinja2  
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5, Font Awesome  
- **Tools:** FFmpeg, ElevenLabs API, `os`, `uuid`, `subprocess`, `threading`

---

## **How It Works**

1. **User Interaction**  
   The user visits `/create`, uploads images, and enters a voiceover text.

2. **Request Handling**  
   `main.py` (Flask app) receives form data and files, saving them into a uniquely named folder under `user_uploads`.

3. **Background Processing**  
   `generate_process.py`, a continuously running script, detects the new upload.

4. **Audio Generation**  
   The script reads `desc.txt` and converts it into `audio.mp3` using the **ElevenLabs API**.

5. **Video Creation**  
   An FFmpeg command combines images from `input.txt` with `audio.mp3`, scaling and cropping for vertical format.

6. **Final Output**  
   The final MP4 reel is saved to `static/reels` and becomes visible in the gallery.

---

## **Version**

### **v1.0 – Initial Launch**
- Core Flask-based website built
- Functional upload and reel generation system added
- Basic UI created with Bootstrap

### **v1.1 – Gallery Refinement**
- Improved `gallery.html` to dynamically display completed reels
- Enhanced styling and layout of the gallery section
- Reel thumbnails and links made more accessible

---



