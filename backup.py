import os
from PIL import Image
import fitz  # PyMuPDF
import zipfile
import shutil
import tempfile

def get_file_size(path):
    """Mengembalikan ukuran file dalam KB"""
    size = os.path.getsize(path)
    return size / 1024  # KB

def compress_office_file(original_path):
    """
    Kompres file DOCX/PPTX dengan mengurangi ukuran gambar di dalamnya.
    """
    temp_dir = tempfile.mkdtemp()
    temp_output = os.path.join(temp_dir, os.path.basename(original_path))
    shutil.copyfile(original_path, temp_output)

    # Extract isi file
    extract_dir = os.path.join(temp_dir, "extracted")
    with zipfile.ZipFile(temp_output, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    # Kompres gambar di dalam folder media
    media_dir = os.path.join(extract_dir, "word", "media")
    if not os.path.exists(media_dir):
        media_dir = os.path.join(extract_dir, "ppt", "media")
    if os.path.exists(media_dir):
        for img_file in os.listdir(media_dir):
            img_path = os.path.join(media_dir, img_file)
            try:
                img = Image.open(img_path)
                img.save(img_path, optimize=True, quality=60)
            except Exception:
                pass

    # Buat file baru dari hasil ekstrak
    output_path = os.path.join(temp_dir, "compressed_" + os.path.basename(original_path))
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as new_zip:
        for root_dir, _, files in os.walk(extract_dir):
            for file in files:
                full_path = os.path.join(root_dir, file)
                relative_path = os.path.relpath(full_path, extract_dir)
                new_zip.write(full_path, relative_path)

    return output_path

def kompres_file(path, kualitas):
    """
    Fungsi utama untuk kompresi file berdasarkan ekstensi dan kualitas.
    """
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext in ['.jpg', '.jpeg', '.png']:
            kualitas_map = {"Tinggi": 80, "Sedang": 50, "Rendah": 30}
            img = Image.open(path)
            output_path = os.path.join(tempfile.gettempdir(), "compressed_" + os.path.basename(path))
            img.save(output_path, quality=kualitas_map[kualitas], optimize=True)
            return output_path

        elif ext == '.pdf':
            doc = fitz.open(path)
            output_path = os.path.join(tempfile.gettempdir(), "compressed_" + os.path.basename(path))
            doc.save(output_path, deflate=True)
            return output_path

        elif ext in ['.docx', '.pptx']:
            return compress_office_file(path)

        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None
