import os
import subprocess

from load_config import (
    AUDIO_OUTPUT_DIR,
    TEXT_INPUT_DIR,
    TTS_MODEL_PATH,
    WORDS_PER_CHUNK,
)


def split_text(text, max_words=WORDS_PER_CHUNK):
    """Split text into chunks of up to max_words."""
    words = text.split()
    chunks = [
        " ".join(words[i : i + max_words]) for i in range(0, len(words), max_words)
    ]
    return chunks


os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)

for filename in sorted(os.listdir(TEXT_INPUT_DIR)):
    if filename.endswith(".txt"):
        txt_path = os.path.join(TEXT_INPUT_DIR, filename)
        base_name = filename.split(".")[0]
        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = split_text(text)

        for i, chunk in enumerate(chunks):
            chunk_filename = f"{base_name}_part{i + 1}.wav"
            wav_path = os.path.join(AUDIO_OUTPUT_DIR, chunk_filename)
            cmd = ["piper-tts", "--model", TTS_MODEL_PATH, "--output_file", wav_path]
            print(f"Generating: {chunk_filename}")
            subprocess.run(cmd, input=chunk.encode("utf-8"), check=True)

print("✅ All files processed.")
