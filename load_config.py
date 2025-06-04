import json

# Load config once and expose variables directly
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Expose clearly named config variables
TEXT_INPUT_DIR = config["text_input_directory"]
AUDIO_OUTPUT_DIR = config["audio_output_directory"]
TTS_MODEL_PATH = config["tts_model_path"]
WORDS_PER_CHUNK = config["chunk_size_words"]
