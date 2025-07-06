import json

# Load config once and expose variables directly
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Required
CHAPTER_OUTPUT_DIR = config.get("chapter_output_directory", "plain_text_chapters")
TEXT_INPUT_DIR = config["text_input_directory"]
AUDIO_OUTPUT_DIR = config["audio_output_directory"]
TTS_MODEL_PATH = config["tts_model_path"]

# Optional
WORDS_PER_CHUNK = config.get("chunk_size_words", 500)
MAX_FILES = config.get("max_files", None)
PIPER_EXECUTABLE_PATH = config.get("piper_executable_path", None)
