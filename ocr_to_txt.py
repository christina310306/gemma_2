import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import numpy as np
import cv2

NOTES_PATH = r"C:\Users\chris\OneDrive\NOTES"
OCR_OUT = os.path.join(NOTES_PATH, "OCR_OUTPUT")

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

os.makedirs(OCR_OUT, exist_ok=True)

def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.adaptiveThreshold(
    gray,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    31,
    2
)

    return gray

def ocr_pdf(path):
    text = ""
    doc = fitz.open(path)
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img = preprocess(np.array(img))
        text += pytesseract.image_to_string(img, config="--psm 4 --oem 3")
    return text

def ocr_image(path):
    img = cv2.imread(path)
    if img is None:
        return ""
    img = preprocess(img)
    return pytesseract.image_to_string(img, config="--psm 4 --oem 3")

for root, _, files in os.walk(NOTES_PATH):
    for f in files:
        src = os.path.join(root, f)
        if f.lower().endswith(".pdf"):
            text = ocr_pdf(src)
        elif f.lower().endswith((".png", ".jpg", ".jpeg")):
            text = ocr_image(src)
        else:
            continue

        if text.strip():
            out = os.path.join(OCR_OUT, f + ".txt")
            with open(out, "w", encoding="utf-8") as w:
                w.write(text)
            print(f"✅ OCR saved: {out}")
