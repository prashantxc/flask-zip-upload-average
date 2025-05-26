import os
import zipfile
import tempfile
import shutil
from flask import Flask, render_template, request
from average_logic import process_folder

app = Flask(__name__)

# Temporary folder for uploads
UPLOAD_FOLDER = tempfile.mkdtemp()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        file = request.files.get("zipfile")
        if not file or file.filename == "":
            result = "No file uploaded."
        elif not file.filename.endswith(".zip"):
            result = "Please upload a .zip file."
        else:
            try:
                # Clear previous files
                for filename in os.listdir(UPLOAD_FOLDER):
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)

                # Save and extract new ZIP
                zip_path = os.path.join(UPLOAD_FOLDER, "uploaded.zip")
                file.save(zip_path)
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(UPLOAD_FOLDER)

                # Process extracted folder
                result = process_folder(UPLOAD_FOLDER)
            except Exception as e:
                result = f"Error: {str(e)}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
