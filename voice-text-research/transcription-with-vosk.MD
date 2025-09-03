# Offline transcription with Vosk

This folder contains two transcription scripts:

- `voice.py` — example using Google Speech Recognition via `SpeechRecognition` (online).
- `voice_vosk.py` — offline, faster transcription using Vosk and `pydub`.

## Quick start

1. Activate your virtual environment:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

2. Install required packages (if not already installed):

   ```powershell
   pip install -r requirements.txt
   ```

3. Download a Vosk model (if not already present):

   Visit https://alphacephei.com/vosk/models and download `vosk-model-small-en-us-0.15.zip`, then unzip it into this folder so you have a directory named `vosk-model-small-en-us-0.15`.

   Or run the included download command in PowerShell (will overwrite if present):

   ```powershell
   Invoke-WebRequest -Uri 'https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip' -OutFile 'vosk-model-small-en-us-0.15.zip'
   Expand-Archive -Path 'vosk-model-small-en-us-0.15.zip' -DestinationPath . -Force
   ```

4. Run the offline transcription:

   ```powershell
   python voice_vosk.py path\to\your_audio.wav
   ```

## Options

- `--model` or `-m` — path to the Vosk model directory (defaults to `vosk-model-small-en-us-0.15` in the project folder).
- `--out` or `-o` — specify output file path for the transcription.
- `--quiet` or `-q` — suppress progress output.

## Notes

- Installing `ffmpeg` and adding it to your PATH will make `pydub` conversions faster and more reliable.
- For better accuracy, try a larger Vosk model or an alternative like Whisper (if you have a GPU).