from flask import Flask, request, jsonify, render_template
import os
import uuid
from werkzeug.utils import secure_filename
from src.config import DATA_UPLOAD

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = DATA_UPLOAD
os.makedirs(DATA_UPLOAD, exist_ok=True)

ALLOWED_EXTENSIONS = {'gpx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '沒有檔案欄位'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '未選擇檔案'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': '只允許上傳 .gpx 檔案'}), 400

    # 取得原始檔名並加入 UUID
    original_filename = secure_filename(file.filename)
    base, ext = os.path.splitext(original_filename)
    unique_filename = f"{base}_{uuid.uuid4().hex}{ext}"
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

    file.save(save_path)

    return jsonify({
        'message': f'{original_filename} 上傳成功，儲存為 {unique_filename}',
        'original_filename': original_filename,
        'saved_filename': unique_filename,
        'saved_to': save_path
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
