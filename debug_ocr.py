import os

OCR_PATH = r"C:\Users\chris\OneDrive\NOTES\OCR_OUTPUT"

print("\n🔎 DEBUGGING OCR CONTENT\n")

for file in os.listdir(OCR_PATH):
    if file.lower().endswith(".txt"):
        path = os.path.join(OCR_PATH, file)
        print(f"\n📄 FILE: {file}")
        print("-" * 40)

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read().lower()

        # Look for certificate-related words
        keywords = [
            "certificate", "certify", "certified",
            "successfully completed", "issued",
            "award", "completion"
        ]

        found = False
        for k in keywords:
            if k in text:
                print(f"✅ FOUND keyword: {k}")
                found = True

        if not found:
            print("❌ NO certificate-related text found")

        # Print first 10 lines for inspection
        print("\n--- SAMPLE TEXT ---")
        print("\n".join(text.splitlines()[:10]))
