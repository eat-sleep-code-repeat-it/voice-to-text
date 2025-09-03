# Google speech vs. Whisper vs. Vosk

```bash
# Relative path (file in the same folder) no json
python voice_whisper.py mmba-ai-programmers-01-01-the-big-three.wav  --json NUL
python voice_whisper.py mmba-ai-programmers-01-02-LLM.wav  --json NUL
python voice_whisper.py mmba-ai-programmers-01-03-prompting.wav  --json NUL

python voice_whisper.py mmba-ai-programmers-02-01-structured-output.wav  --json NUL

python voice_whisper.py mmba-ai-programmers-03-01-RAG.wav  --json NUL
python voice_whisper.py mmba-ai-programmers-03-02-embedding-documents.wav  --json NUL

python voice_whisper.py mmba-ai-programmers-04-01-observability.wav  --json NUL
python voice_whisper.py mmba-ai-programmers-04-02-evaluations.wav  --json NUL
python voice_whisper.py mmba-ai-programmers-04-03-guardrails.wav  --json NUL

python voice_whisper.py mmba-ai-programmers-05-01-chaining.wav  --json NUL
python voice_whisper.py mmba-ai-programmers-05-02-human-in-the-loop.wav  --json NUL

python voice_whisper.py mmba-ai-programmers-06-01-ai-with-git.wav  --json NUL
python voice_whisper.py mmba-ai-programmers-06-02-advanced-cursor.wav  --json NUL

python voice_whisper.py mmba-ai-programmers-07-01-project-week.mp3
python voice_whisper.py mmba-ai-programmers-07-02-project-week.wav
```

## how to run each of of them
```bash
# Run default bundled audio and default model (base in the script)
python voice_whisper.py mmba-ai-programmers-01-01-the-big-three.wav

# Run with a specific model (faster → tiny, more accurate → medium/large):
python voice_whisper.py mmba-ai-programmers-01-01-the-big-three.wav --model tiny
python voice_whisper.py mmba-ai-programmers-01-01-the-big-three.wav --model base
python voice_whisper.py mmba-ai-programmers-01-01-the-big-three.wav --model small
python voice_whisper.py mmba-ai-programmers-01-01-the-big-three.wav --model medium
python voice_whisper.py mmba-ai-programmers-01-01-the-big-three.wav --model large

# Absolute path
python voice_whisper.py 'C:\path\to\your file.mp3'

# Specify model
python voice_whisper.py 'C:\path\to\audio.mp3' --model small
```

- Google (the recognize_google call in voice.py): Not strictly a supported paid API — it uses Google’s free web speech endpoint and works for light/testing but is undocumented and rate-limited (not guaranteed). For reliable, production use you must use Google Cloud Speech-to-Text, which is a paid service.
- Whisper (local via openai-whisper): Free to run locally — the Whisper code/models are open-source (MIT). No usage fees for local runs, but large models require substantial CPU/GPU time and memory (your hardware cost). Note: OpenAI’s hosted Whisper API (if used) is a paid service.
- Vosk (local):Free — open-source (Apache 2.0). No service fees; runs entirely on your machine. Caveat: model download size and local compute used by your CPU/GPU are your resource cost.

Privacy note: Vosk and local Whisper keep audio on your machine; Google sends audio to Google servers.

If you want a private, no-cost option, run Whisper or Vosk locally; if you want a managed paid service with SLA, use Google Cloud Speech or a paid Whisper/OpenAI API. Which direction do you prefer?

If you value absolute accuracy and are okay using the online Google API, voice.py (Google) produced the best result for this audio.

If you prefer a local solution with good accuracy and faster runtime, Whisper base is a strong choice.

For offline and fastest option, Vosk is fastest but less accurate.



