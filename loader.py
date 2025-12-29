import os

def load_notes(notes_path):
    chunks = []

    # 1️⃣ Load normal text files
    for root, _, files in os.walk(notes_path):
        for file in files:
            path = os.path.join(root, file)

            if file.lower().endswith(".txt"):
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        text = f.read().strip()
                        if text:
                            chunks.extend(split_chunks(text))
                except Exception as e:
                    print(f"⚠️ Skipped {file}: {e}")

    # 2️⃣ Load OCR output explicitly
    ocr_path = os.path.join(notes_path, "OCR_OUTPUT")
    if os.path.exists(ocr_path):
        for file in os.listdir(ocr_path):
            if file.lower().endswith(".txt"):
                path = os.path.join(ocr_path, file)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        text = f.read().strip()
                        if text:
                            chunks.extend(split_chunks(text))
                except Exception as e:
                    print(f"⚠️ Skipped OCR {file}: {e}")

    return chunks


def split_chunks(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks
