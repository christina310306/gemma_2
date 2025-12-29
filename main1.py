import os
from rank_bm25 import BM25Okapi
from local_llm import ask_gemma  # local Gemma via Ollama
from loader import load_notes   # loads text chunks from NOTES

# ---------------- CONFIG ----------------
NOTES_PATH = r"C:\Users\chris\OneDrive\NOTES"
MIN_RELEVANCE = 4.0   # 🔑 this fixes your problem
TOP_K = 3

# ---------------- SEARCH ----------------
def build_bm25(chunks):
    tokenized = [c.lower().split() for c in chunks]
    return BM25Okapi(tokenized)

def search_notes(bm25, chunks, question):
    scores = bm25.get_scores(question.lower().split())
    best_idx = max(range(len(scores)), key=lambda i: scores[i])
    return chunks[best_idx], scores[best_idx]

# ---------------- MAIN ----------------
def main():
    print("📂 Loading OneDrive notes...")
    chunks = load_notes(NOTES_PATH)

    if not chunks:
        print("❌ No notes found in OneDrive")
        return

    print(f"📚 Loaded {len(chunks)} chunks")

    bm25 = build_bm25(chunks)

    print("\n🧠 Hybrid Search + Gemma ready")
    print("Type 'exit' to quit\n")

    while True:
        question = input("❓ Question: ").strip()

        if not question:
            continue

        if question.lower() in ("exit", "quit"):
            print("👋 Exiting cleanly.")
            break

        # -------- SEARCH --------
        best_chunk, best_score = search_notes(bm25, chunks, question)

        print(f"🧪 DEBUG → BM25 score: {best_score:.2f}")

        # -------- DECISION LOGIC --------
        if best_score >= MIN_RELEVANCE:
            # Try answering from OneDrive
            prompt = f"""
You are given content extracted from my OneDrive notes.

If the content contains relevant code or implementation details,
extract and present them clearly.
If the code is partial or noisy, reconstruct it as best as possible.
If nothing relevant exists, say: NOT FOUND IN ONEDRIVE.

CONTENT:
{best_chunk}

QUESTION:
{question}
"""

            try:
                answer = ask_gemma(prompt)
            except Exception as e:
                print("⚠️ Gemma error:", e)
                answer = ""

            # Weak / refusal detection → GK fallback
            if (not answer or
                "not found" in answer.lower() or
                "does not include" in answer.lower() or
                "cannot answer" in answer.lower()):

                print("\n❌ Not found in OneDrive")
                print("🌍 General knowledge:\n")
                print(ask_gemma(question))

            else:
                print("\n🤖 Answer (from OneDrive):\n")
                print(answer)

        else:
            # Low relevance → GK fallback directly
            print("\n❌ Not found in OneDrive")
            print("🌍 General knowledge:\n")
            print(ask_gemma(question))

        print("\n" + "-" * 60 + "\n")

# ---------------- RUN ----------------
if __name__ == "__main__":
    main()
