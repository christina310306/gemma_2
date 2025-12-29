import subprocess

def ask_gemma(prompt: str) -> str:
    try:
        process = subprocess.run(
            ["ollama", "run", "gemma"],
            input=prompt,
            text=True,
            encoding="utf-8",
            errors="ignore",
            capture_output=True,
            
        )
        return process.stdout.strip()
    except Exception as e:
        return f"⚠️ Gemma error: {e}"
