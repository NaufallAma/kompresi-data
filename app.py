from flask import Flask, render_template, request, redirect, send_file, url_for
import os
import tempfile
import shutil
from kompres import kompres_file, get_file_size

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), "kompresor_upload")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        kualitas = request.form.get('kualitas')

        if not file or not kualitas:
            return render_template('index.html', error="File dan kualitas wajib diisi.")

        # Simpan file sementara
        original_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(original_path)

        # Kompres file
        hasil_path = kompres_file(original_path, kualitas)
        if not hasil_path:
            return render_template('index.html', error="Kompresi gagal atau format tidak didukung.")

        # Hitung ukuran
        before = get_file_size(original_path)
        after = get_file_size(hasil_path)

        # Simpan nama file hasil untuk download
        download_name = os.path.basename(hasil_path)
        shutil.copyfile(hasil_path, os.path.join(UPLOAD_FOLDER, download_name))

        return render_template('index.html',
                               nama_file=file.filename,
                               before_size=f"{before:.2f} KB",
                               after_size=f"{after:.2f} KB",
                               download_url=url_for('download_file', filename=download_name))

    return render_template('index.html')


@app.route('/download/<filename>')
def download_file(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "File tidak ditemukan", 404

if __name__ == '__main__':
    app.run(debug=True)
