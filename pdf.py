import fitz  # pip install pymupdf
import tkinter as tk
import json
from tkinter import filedialog
import os

def add_bookmarks(input_path, output_path, bookmarks):
    doc = fitz.open(input_path)
    toc = []

    for page_num_str, bookmark_info in bookmarks.items():
        page_num = int(page_num_str)
        level = bookmark_info["level"]
        title = bookmark_info["title"]
        toc.append([level, title, page_num])

    doc.set_toc(toc)
    doc.save(output_path)
    doc.close()

def select_files_and_add_bookmarks():
    root = tk.Tk()
    root.withdraw()

    json_file = "data.json"
    if not os.path.exists(json_file):
        print("Không tìm thấy file 'data.json' trong thư mục hiện tại.")
        return

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            bookmarks = json.load(f)
    except Exception as e:
        print(f"Lỗi khi đọc 'data.json': {e}")
        return

    input_file = filedialog.askopenfilename(
        title="Chọn file PDF đầu vào",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if not input_file:
        print("Không có file PDF nào được chọn. Đang hủy...")
        return

    default_name = os.path.basename(input_file)

    # Tạo thư mục json_backup nếu chưa có
    backup_dir = "json_backup"
    os.makedirs(backup_dir, exist_ok=True)

    # Lưu bản sao data.json vào json_backup với tên file PDF
    pdf_name_without_ext = os.path.splitext(default_name)[0]
    backup_json_path = os.path.join(backup_dir, f"{pdf_name_without_ext}.json")
    try:
        with open(backup_json_path, 'w', encoding='utf-8') as f:
            json.dump(bookmarks, f, ensure_ascii=False, indent=4)
        print(f"✅ Đã lưu bản sao data.json vào: {backup_json_path}")
    except Exception as e:
        print(f"❌ Lỗi khi lưu bản sao: {e}")
        return

    output_file = filedialog.asksaveasfilename(
        title="Lưu file PDF đầu ra",
        defaultextension=".pdf",
        initialfile=default_name,
        filetypes=[("PDF Files", "*.pdf")]
    )
    if not output_file:
        print("Không chọn vị trí lưu file. Đang hủy...")
        return

    add_bookmarks(input_file, output_file, bookmarks)
    print(f"✅ Đã thêm bookmarks và lưu vào: {output_file}")

# Gọi hàm chính
if __name__ == "__main__":
    select_files_and_add_bookmarks()
