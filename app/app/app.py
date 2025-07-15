from flask import Flask, request, redirect, url_for, jsonify
import os
from src.config import DATA_UPLOAD

app = Flask(__name__)

# 設定上傳的檔案儲存路徑（可選）

os.makedirs(DATA_UPLOAD, exist_ok=True)
app.config['UPLOAD_FOLDER'] = DATA_UPLOAD

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '沒有檔案欄位'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': '未選擇檔案'}), 400

    # 儲存檔案（可選）
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(save_path)

    return jsonify({
        'message': '上傳成功',
        'filename': file.filename,
        'saved_to': save_path
    })


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
