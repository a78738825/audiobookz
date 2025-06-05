import os
import subprocess
from pathlib import Path

from load_config import AUDIO_OUTPUT_DIR, TEXT_INPUT_DIR, TTS_MODEL_PATH


def generate_audio_from_text_files():
    input_path = Path(TEXT_INPUT_DIR)
    output_path = Path(AUDIO_OUTPUT_DIR)
    model_path = Path(TTS_MODEL_PATH).expanduser()

    # Ensure output directory exists
    output_path.mkdir(parents=True, exist_ok=True)

    # Get all .txt files in input directory
    for txt_file in sorted(input_path.glob("*.txt")):
        output_filename = txt_file.stem + ".wav"
        output_file_path = output_path / output_filename

        # Skip if output already exists
        if output_file_path.exists():
            print(f"Skipping {txt_file.name}, output already exists.")
            continue

        try:
            print(f"Generating audio for {txt_file.name}...")
            with open(txt_file, "r", encoding="utf-8") as f:
                text = f.read()

            process = subprocess.run(
                [
                    "piper-tts",
                    "--model",
                    str(model_path),
                    "--output_file",
                    str(output_file_path),
                ],
                input=text,
                text=True,
                capture_output=True,
            )

            if process.returncode != 0:
                print(f"Error generating audio for {txt_file.name}: {process.stderr}")
            else:
                print(f"Successfully created: {output_file_path.name}")

        except Exception as e:
            print(f"Exception while processing {txt_file.name}: {e}")


if __name__ == "__main__":
    generate_audio_from_text_files()
