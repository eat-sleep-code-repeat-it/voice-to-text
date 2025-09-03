#!/usr/bin/env python3
"""Local OpenAI Whisper transcription helper.

Requires: openai-whisper (pip package) and torch. Install with:
  pip install -U openai-whisper torch

This script converts input audio to a supported WAV (via pydub/ffmpeg if needed),
runs Whisper locally, and writes plain text and JSON segment output.
"""
import os
import sys
import json
import argparse
import tempfile
try:
    import whisper
except Exception as e:
    print("Missing dependency 'openai-whisper'. Install with: pip install -U openai-whisper")
    raise

from pydub import AudioSegment


def ensure_audio_wav(src_path):
    # Whisper accepts many formats, but converting to a WAV with ffmpeg ensures
    # predictable behavior and sampling rate.
    ext = os.path.splitext(src_path)[1].lower()
    if ext == '.wav':
        return src_path
    audio = AudioSegment.from_file(src_path)
    tmp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    # whisper will handle resampling internally; export as 16-bit WAV
    audio.export(tmp.name, format='wav')
    return tmp.name


def transcribe(model_size, src, out_txt=None, out_json=None, device=None):
    wav = ensure_audio_wav(src)
    print(f"Loading Whisper model: {model_size} (this may take a while)")
    model = whisper.load_model(model_size)
    print("Transcribing...")
    result = model.transcribe(wav)

    text = result.get('text', '')
    if out_txt is None:
        out_txt = os.path.splitext(os.path.basename(src))[0] + f"_whisper_{model_size}.txt"
    with open(out_txt, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Saved text to', out_txt)

    if out_json is None:
        out_json = os.path.splitext(os.path.basename(src))[0] + f"_whisper_{model_size}.json"

    # result already contains `segments` with start/end and text when available
    with open(out_json, 'w', encoding='utf-8') as jf:
        json.dump(result, jf, ensure_ascii=False, indent=2)
    print('Saved JSON to', out_json)

    # cleanup temp wav if created
    if wav != src:
        try:
            os.remove(wav)
        except Exception:
            pass


def main():
    p = argparse.ArgumentParser(description='Transcribe audio locally with OpenAI Whisper')
    p.add_argument('audio', nargs='?', default=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mmba-ai-programmers-01-01-the-big-three.wav'))
    p.add_argument('--model', '-m', default='base', help='Whisper model size to load (tiny, base, small, medium, large)')
    p.add_argument('--out', '-o', help='Output text filename')
    p.add_argument('--json', nargs='?',  default='NUL', help='Output JSON filename')
    args = p.parse_args()

    if not os.path.exists(args.audio):
        print('Audio file not found:', args.audio)
        sys.exit(1)

    transcribe(args.model, args.audio, out_txt=args.out, out_json=args.json)


if __name__ == '__main__':
    main()
