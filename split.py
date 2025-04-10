import fitz  # pip install pymupdf
import tkinter as tk
from tkinter import filedialog

def split_pdf(input_path, output_path, start_page, end_page):
    doc = fitz.open(input_path)

    # Giảm 1 vì fitz bắt đầu từ trang 0
    start = start_page - 1
    end = end_page

    if start < 0 or end > len(doc) or start >= end:
        print(f"❌ Lỗi: khoảng trang không hợp lệ (file có {len(doc)} trang).")
        return

    new_doc = fitz.open()
    for i in range(start, end):
        new_doc.insert_pdf(doc, from_page=i, to_page=i)

    new_doc.save(output_path)
    new_doc.close()
    doc.close()

    print(f"✅ Đã lưu đoạn PDF từ trang {start_page} đến {end_page} vào: {output_path}")


if __name__ == "__main__":
    # Mở hộp thoại chọn file
    root = tk.Tk()
    root.withdraw()
    input_file = filedialog.askopenfilename(
        title="Chọn file PDF để cắt",
        filetypes=[("PDF files", "*.pdf")]
    )

    if not input_file:
        print("❌ Không có file nào được chọn.")
        exit()

    print(f"📄 Đã chọn: {input_file}")

    # Nhập trang bắt đầu và kết thúc từ CLI
    try:
        start_page = int(input("Nhập trang bắt đầu: "))
        end_page = int(input("Nhập trang kết thúc: "))
    except ValueError:
        print("❌ Trang phải là số nguyên.")
        exit()

    # Tạo tên file đầu ra
    output_file = f"split_{start_page}_{end_page}.pdf"

    # Gọi hàm split
    split_pdf(input_file, output_file, start_page, end_page)
