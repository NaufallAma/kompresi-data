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

def compress_office_file(original_path, kualitas):
    """
    Kompres file DOCX/PPTX dengan mengurangi ukuran gambar di dalamnya
    berdasarkan parameter kualitas.
    """
    kualitas_map = {"Tinggi": 80, "Sedang": 60, "Rendah": 40}

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
                img.convert("RGB").save(img_path, optimize=True, quality=kualitas_map[kualitas])
            except Exception as e:
                print("Gagal kompres gambar di file Office:", e)

    # Buat file baru dari hasil ekstrak
    output_path = os.path.join(tempfile.gettempdir(), "compressed_" + os.path.basename(original_path))
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as new_zip:
        for root_dir, _, files in os.walk(extract_dir):
            for file in files:
                full_path = os.path.join(root_dir, file)
                relative_path = os.path.relpath(full_path, extract_dir)
                new_zip.write(full_path, relative_path)

    shutil.rmtree(temp_dir)
    return output_path

def kompres_file(path, kualitas):
    """
    Fungsi utama untuk kompresi file berdasarkan ekstensi dan kualitas.
    """
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext in ['.jpg', '.jpeg']:
            kualitas_map = {"Tinggi": 80, "Sedang": 50, "Rendah": 30}
            img = Image.open(path)
            output_path = os.path.join(tempfile.gettempdir(), "compressed_" + os.path.basename(path))
            img.convert("RGB").save(output_path, format='JPEG', quality=kualitas_map[kualitas], optimize=True)
            return output_path

        elif ext == '.png':
            # PNG tidak pakai kualitas, hanya optimize (lossless)
            img = Image.open(path)
            output_path = os.path.join(tempfile.gettempdir(), "compressed_" + os.path.basename(path))
            img.save(output_path, format='PNG', optimize=True)
            return output_path

        elif ext == '.pdf':
            doc = fitz.open(path)
            output_path = os.path.join(tempfile.gettempdir(), "compressed_" + os.path.basename(path))
            doc.save(output_path, deflate=True)
            return output_path

        elif ext in ['.docx', '.pptx']:
            return compress_office_file(path, kualitas)

        else:
            print("Format tidak didukung:", ext)
            return None

    except Exception as e:
        print("Error saat kompresi:", e)
        return None
