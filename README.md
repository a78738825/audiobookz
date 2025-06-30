# 📚 EPUB to Audiobook Converter

Convert `.epub` ebooks into clean text — then into spoken audio using local text-to-speech (TTS) with [Piper TTS](https://github.com/rhasspy/piper).

This project consists of:

* 📝 `epub_to_text.py` – extracts plain text chapters from an EPUB file
* 🔊 `generate_audio.py` – turns text chapters into `.wav` files using Piper
* ⚙️ A flexible `config.json` to control everything

---

## ⚙️ Configuration

All settings live in `config.json`:

```json
{
  "text_input_directory": "tmp",
  "audio_output_directory": "audio_output",
  "tts_model_path": "models/en_US-hfc_male-medium.onnx",
  "chunk_size_words": 500,
  "max_files": 10,
  "piper_executable_path": "/usr/bin/piper-tts"
}
```

### Explanation of keys:

| Key                      | Description                                                               |
| ------------------------ | ------------------------------------------------------------------------- |
| `text_input_directory`   | Folder where `.txt` files will be read from by the audio generator        |
| `audio_output_directory` | Folder where `.wav` output will be saved                                  |
| `tts_model_path`         | Path to your `.onnx` voice model                                          |
| `chunk_size_words`       | (Currently unused) Reserved for future: splitting long chapters           |
| `max_files`              | Limits how many `.txt` files get processed (e.g. 10 chapters at a time)   |
| `piper_executable_path`  | Absolute path to your Piper binary — or leave unset to use system install |

---

## 💡 Why the `tmp/` Folder?

To avoid overwhelming your system by processing *every chapter at once*, you can:

1. Run `epub_to_text.py` to extract **all** chapter `.txt` files into `plain_text_chapters/`
2. Copy just a **subset** (e.g., 10–15) into `tmp/`
3. Set `"text_input_directory": "tmp"` in your config
4. Run `generate_audio.py` to create audio only for those

This gives you **manual control** over which chapters are processed.

### 🔒 Future idea:

A more elegant solution could support:

* `include_files`: explicitly list chapters to include
* `random_sample`: randomly select a few for preview
* `skip_existing`: true (already implemented)

---

## 📦 Directory Structure (after use)

```
.
├── config.json                  # All paths & behavior defined here
├── epub_to_text.py              # Extracts chapter-wise text from .epub
├── generate_audio.py            # Converts text to audio using Piper
├── load_config.py               # Handles config parsing
├── models/
│   ├── en_US-hfc_male-medium.onnx
│   └── en_US-hfc_male-medium.onnx.json
├── plain_text_chapters/         # Full output of epub_to_text.py
├── tmp/                         # Temp folder for selected chapters
├── audio_output/                # Output folder for audio files
├── requirements.txt             # Python dependencies
└── venv/                        # (Optional) Python virtualenv
```

🟡 You're free to **rename**, **reorganize**, or **move** things — as long as `config.json` points to the correct locations.

---

## 🛠️ Setup

### 1. Install Python dependencies

```bash
python3 -m venv venv
pip install -r requirements.txt
```

---

### 2. Install Piper (and download a model)

You have **two main options** for using Piper:

#### 🔧 Option A: System install

Follow [Piper’s official instructions](https://github.com/rhasspy/piper#installation).

Example for **Arch Linux** (btw):

```bash
paru -S piper-tts-bin
```

Once installed, the binary will likely be available globally as `piper-tts`.

#### 📦 Option B: Download release binary manually

If you don’t want to install Piper system-wide:

1. Visit the [Piper Releases](https://github.com/rhasspy/piper/releases) page

2. Download the appropriate binary archive for your OS (e.g. `piper-linux-x86_64.tar.gz`)

3. Extract it anywhere (e.g. in your project under `./bin/`):

   ```bash
   mkdir -p bin
   tar -xvf piper-linux-x86_64.tar.gz -C bin/
   ```

4. Update `config.json`:

   ```json
   "piper_executable_path": "bin/piper"
   ```

Now the script will use your local binary instead of requiring a global installation.

---

### ✅ Also download a voice model

You’ll need to download a `.onnx` model file (and its `.json` config) for the voice you'd like.

Example:

* Model: `en_US-hfc_male-medium.onnx`
* Config: `en_US-hfc_male-medium.onnx.json`
* Place both in your `models/` directory
* Set the path in `config.json`:

```json
"tts_model_path": "models/en_US-hfc_male-medium.onnx"
```

Make sure both files are side by side, as Piper expects the `.json` config next to the model unless told otherwise.

---

## 🚀 Usage

### Step 1: Convert EPUB to Text

```bash
python epub_to_text.py
```

➡️ Prompts for an `.epub` file
➡️ Outputs `.txt` chapters to `plain_text_chapters/`

---

### Step 2: Convert Text to Audio

Make sure `text_input_directory` is set (e.g. to `tmp/` or `plain_text_chapters/`) in `config.json`, then:

```bash
python generate_audio.py
```

➡️ Converts all `.txt` files (up to `max_files`)
➡️ Saves `.wav` files in `audio_output/`
➡️ Skips already existing files

---

## 📘 FAQ

**Q: Can I use a custom path to Piper binary?**
✅ Yes. Just set `piper_executable_path` in `config.json`.

**Q: Can I limit how many chapters get processed?**
✅ Use `max_files` or manually copy files to `tmp/`.

**Q: Can I rename folders and still run the scripts?**
✅ Absolutely — just update the paths in `config.json`.

---

## 📜 License

MIT — do whatever you want, but attribution is appreciated.
