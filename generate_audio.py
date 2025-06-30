import subprocess
from pathlib import Path

from load_config import (
    AUDIO_OUTPUT_DIR,
    MAX_FILES,
    PIPER_EXECUTABLE_PATH,
    TEXT_INPUT_DIR,
    TTS_MODEL_PATH,
)


def generate_audio_from_text_files():
    input_path = Path(TEXT_INPUT_DIR)
    output_path = Path(AUDIO_OUTPUT_DIR)
    model_path = Path(TTS_MODEL_PATH).expanduser()
    piper_executable = (
        Path(PIPER_EXECUTABLE_PATH).expanduser()
        if PIPER_EXECUTABLE_PATH
        else "piper-tts"
    )

    # Ensure output directory exists
    output_path.mkdir(parents=True, exist_ok=True)

    # Gather all .txt files
    txt_files = sorted(input_path.glob("*.txt"))

    # If a max file limit is set, apply it
    if isinstance(MAX_FILES, int) and MAX_FILES > 0:
        txt_files = txt_files[:MAX_FILES]

    for txt_file in txt_files:
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
                    str(piper_executable),
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
                print(
                    f"❌ Error generating audio for {txt_file.name}:\n{process.stderr.strip()}"
                )
            else:
                print(f"✅ Successfully created: {output_file_path.name}")

        except Exception as e:
            print(f"⚠️ Exception while processing {txt_file.name}: {e}")


if __name__ == "__main__":
    generate_audio_from_text_files()
