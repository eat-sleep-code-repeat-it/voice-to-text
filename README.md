# Voice to text transcription

```bash
uv venv
.venv\Scripts\activate

uv pip install git+https://github.com/openai/whisper.git torch
uv pip install opencc-python-reimplemented
uv pip freeze > requirements.txt

uv run voice_whisper_english.py 
uv run voice_whisper_chinese.py

uv pip install pydub
uv pip freeze > requirements.txt
uv run voice_whisper.py  english-audio.mp3
uv run voice_whisper.py  chinese_audio.mp3
```
