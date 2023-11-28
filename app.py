from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']

        if file1.filename and file2.filename:
            filename1 = secure_filename(file1.filename)
            filename2 = secure_filename(file2.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            return 'Files uploaded successfully'
        else:
            return 'Please select two files before uploading.'
    return 'Failed to upload files'

@app.route('/uploads')
def list_uploads():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('list_uploads.html', files=files)

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
